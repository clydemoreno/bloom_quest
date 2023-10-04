from flask import Flask, jsonify, request
import logging
import asyncio
from pathlib import Path
import sys

import grpc
from concurrent import futures

# Get the root directory of your project
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))


import web.notification_pb2 as my_grpc_pb2
import web.notification_pb2_grpc as my_grpc_pb2_grpc

from db.order_repository import OrderRepository
from reader.bloom_filter_reader import BloomFilterReader
from utility.load_config import load_config
from web.periodic_task import PeriodicTask
from bloom_filter_sha256 import BloomFilter

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Global variables
bf = None
br_subject = None
periodic_task = None


# Load configuration
config_data = load_config()

# Example usage:
def my_callback(message):
    print("my callback got called")
    global br_subject
    if br_subject is not None:
        print("before subject notify")
        asyncio.run(br_subject.notify(f"Event callback executed. {message}"))

# Custom context manager to perform setup only once
class SetupContext:
    def __enter__(self):
        run_grpc_server()

        global periodic_task

        asyncio.run(populate_bloom_filter())

        if periodic_task is None:
            # Create a PeriodicTask instance with your callback
            periodic_task = PeriodicTask(my_callback, interval_seconds=1000)

    def __exit__(self, exc_type, exc_value, traceback):
        pass

# Populate Bloom Filter and BloomFilterReader
async def populate_bloom_filter():
    global bf
    global br_subject

    global config_data
    db_params = config_data["database"]
    fp = config_data["bloom_filter"]["false_positive_probability"]
    size = config_data["bloom_filter"]["size"]

    if bf is None:
        bf = BloomFilter(size, fp)

    if br_subject is None:
        folder_path = str(project_root / config_data["data"]["path"])
        print("folder to watch: ", folder_path)
        br_subject = BloomFilterReader(folder_path)

    await br_subject.attach(bf)

# gRPC service implementation
class NotificationService(my_grpc_pb2_grpc.NotificationServiceServicer):
    def TriggerNotification(self, request, context):
        message = request.message

        # Call br_subject.notify with the provided message
        asyncio.run(br_subject.notify(f"External Notification: {message}"))

        return my_grpc_pb2.NotificationResponse(result="Notification triggered successfully")

@app.before_request
def before_request():
    with SetupContext():
        pass

@app.route('/')
def get_config():
    return jsonify(config_data)

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    db_params = config_data['database']
    global bf

    use_bloom = request.args.get("usebloom")
    if use_bloom == "1" and bf is not None:
        print(f"BF Size in flask is {bf.size}")

        if not bf.check(str(order_id)):
            return jsonify({"error": "Order not found"}), 404

    order_repo = OrderRepository(db_params)
    order = asyncio.run(order_repo.get_order_by_id(order_id))

    if order:
        return jsonify(order)
    else:
        return jsonify({"error": "Order not found"}), 404

# Create and run the gRPC server
def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_grpc_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(), server)
    server.add_insecure_port('[::]:50052')  # Use a different port for gRPC
    server.start()
    print("grpc server started")


if __name__ == '__main__':
    # Start the gRPC server alongside the Flask app
    app.run(debug=True, host='0.0.0.0')
