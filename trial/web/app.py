from flask import Flask, jsonify
import sys
import logging
import asyncio
from pathlib import Path
# import threading
from flask import request

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Declare global variables for bf and br_subject
bf = None
br_subject = None
periodic_task = None

# Create a thread for the periodic task
periodic_thread = None

# Get the root directory of your project (two levels up from web/app.py)
project_root = Path(__file__).resolve().parent.parent

# Add your project's root directory to sys.path
sys.path.append(str(project_root))

from db.order_repository import OrderRepository
from utility.load_config import load_config
from reader.bloom_filter_reader import BloomFilterReader
# from bloom_filter_factory import BloomFilterFactory
from web.periodic_task import PeriodicTask
from bloom_filter_sha256 import BloomFilter

config_data = load_config()

# Example usage:
def my_callback(message):
    print("my callback got called")

def temp_my_callback(message):
    print("my callback got called")
    global br_subject
    if br_subject is not None:
        asyncio.run(br_subject.notify(f"Event callback executed. {message}"))


# Custom context manager to perform setup only once
class SetupContext:
    def __enter__(self):
        global bf
        global br_subject
        global periodic_task  # Use the periodic_task from the main module


        if bf is None:
            size = config_data["bloom_filter"]["size"]
            fp = config_data["bloom_filter"]["false_positive_probability"]
            bf = BloomFilter(size, fp)
            asyncio.run( populate_bloom_filter(bf))

        if br_subject is None:
            folder_path = str(project_root / config_data["data"]["path"])
            print("folder to watch: ", folder_path)
            br_subject = BloomFilterReader(folder_path)
            asyncio.run(br_subject.attach(bf))

        if periodic_task is None:
            # Create a PeriodicTask instance with your callback
            periodic_task = PeriodicTask(my_callback, interval_seconds=30)


    def __exit__(self, exc_type, exc_value, traceback):
        pass

# Call the setup context manager before the first request
async def populate_bloom_filter(bf:BloomFilter):
    global config_data
    db_params = config_data["database"]
    o = OrderRepository(db_params)
    all_orders = await o.get_all_orders()
    for order in all_orders:
        bf.add(order['ID'])

@app.before_request
def before_request():
    with SetupContext():
        pass

@app.route('/')
def get_config():
    return jsonify(config_data)

# @app.route("/orders/<int:order_id>", methods=["GET"])
# def get_order(order_id):
#     db_params = config_data['database']
#     global bf
#     if bf is not None:
#         print("bf: ", bf.check(str(order_id)), bf.check(201) )
#         print(f"BF Size in flask is {bf.size}")
#     if bf is not None and not bf.check(str(order_id)):
#         return jsonify({"error": "Order not found"}), 404
#     else:    
#         order_repo = OrderRepository(db_params)
#         order = asyncio.run(order_repo.get_order_by_id(order_id))
#         if order:
#             return jsonify(order)
#         else:
#             return jsonify({"error": "Order not found"}), 404



@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    db_params = config_data['database']
    global bf

    use_bloom = request.args.get("usebloom")
    if use_bloom == "1" and bf is not None:
        print("bf: ", bf.check(str(order_id)), bf.check(201))
        print(f"BF Size in flask is {bf.size}")

        if not bf.check(str(order_id)):
            return jsonify({"error": "Order not found"}), 404

    order_repo = OrderRepository(db_params)
    order = asyncio.run(order_repo.get_order_by_id(order_id))

    if order:
        return jsonify(order)
    else:
        return jsonify({"error": "Order not found"}), 404



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
