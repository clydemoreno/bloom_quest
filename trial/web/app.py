from flask import Flask, jsonify
import json
import sys
sys.path.append('../async/')

from async_file import AsyncFile  # Import your AsyncFile class
from async_config_loader import AsyncConfigLoader

sys.path.append('../db/')
from order_repository import OrderRepository

app = Flask(__name__)

@app.route('/')
# def get():
#     return "hello"
async def get_config():
    print('here')
    config_loader = AsyncConfigLoader('../async/config.json')
    config_data = await config_loader.load_config_async()
    return jsonify(config_data)

@app.route("/orders/<int:order_id>", methods=["GET"])
async def get_order(order_id):
    config_loader = AsyncConfigLoader('../async/config.json')
    config_data = await config_loader.load_config_async()
    db_params = config_data['database']
    order_repo = OrderRepository(db_params)
    order = await order_repo.get_order_by_id(order_id)
    if order:
        return jsonify(order)
    else:
        return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Add any other desired parameters
