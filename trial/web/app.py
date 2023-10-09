from flask import Flask, jsonify, request
import sys
import logging
import asyncio
from pathlib import Path
from concurrent import futures
# import grpc
import threading  # Import the threading module


# Get the root directory of your project (two levels up from web/app.py)
project_root = Path(__file__).resolve().parent.parent

# Add your project's root directory to sys.path
sys.path.append(str(project_root))


from db.order_repository import OrderRepository
from utility.load_config import load_config
from reader.bloom_filter_reader import BloomFilterReader
from web.periodic_task import PeriodicTask
from bloom_filter_sha256 import BloomFilter
import notification_pb2 as my_grpc_pb2
import notification_pb2_grpc as my_grpc_pb2_grpc
import web.singleton_grpc_service as grpc_service


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Declare global variables for bf, br_subject, and gRPC service
bf = None
br_subject = None
periodic_task = None

grpc_service_instance = None

config_data = load_config()

# Example usage:
def temp_my_callback(message):
    print("my callback got called")

def my_callback(message):
    print("my callback got called")
    global br_subject
    if br_subject is not None:
        print("before subject notify")

        asyncio.run(br_subject.notify(f"Event callback executed. {message}"))

# Define a custom callback function to handle notifications
def custom_notification_callback(message):
    # Customize the notification handling logic here
    print("Custom Notification:", message)
    my_callback(message)
    return "Custom Notification handled successfully"












# Custom context manager to perform setup only once
class SetupContext:
    def __enter__(self):
        global periodic_task, grpc_service

    

        asyncio.run(populate_bloom_filter())

        if periodic_task is None:
            # Create a PeriodicTask instance with your callback
            periodic_task = PeriodicTask(my_callback, interval_seconds=1000)

        # Start the gRPC service in a separate thread
        grpc_thread = threading.Thread(target=run_grpc_server, args=(custom_notification_callback,))
        grpc_thread.start()  # Start the thread


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


def run_grpc_server(notification_callback):
    global grpc_service_instance

    if grpc_service_instance is None:
        grpc_service_instance = grpc_service.SingletonGRPCService(notification_callback)
        grpc_service_instance.start_service()
        grpc_service_instance.wait_for_termination()



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
