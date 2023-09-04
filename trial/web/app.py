from flask import Flask, jsonify
import sys
import logging
# sys.path.append('../async/')

# from async_file import AsyncFile  # Import your AsyncFile class
# from async_config_loader import AsyncConfigLoader

sys.path.append('../db/')
from order_repository import OrderRepository

sys.path.append('../utility')
from load_config import load_config

sys.path.append('../')
from bloom_filter_factory import BloomFilterFactory


app = Flask(__name__)
# Configure the logging level (you can adjust it as needed)
app.logger.setLevel(logging.DEBUG)

config_data = load_config()



bf = BloomFilterFactory.create_from_config(config_data)
bf.add("5")

@app.route('/')
async def get_config():
    # config_loader = AsyncConfigLoader('../async/config.json')
    # config_data = await config_loader.load_config_async()
    return jsonify(config_data)

@app.route("/orders/<int:order_id>", methods=["GET"])
async def get_order(order_id):
    # config_loader = AsyncConfigLoader('../async/config.json')
    # config_data = await config_loader.load_config_async()
    db_params = config_data['database']
    global bf
    if bf is not None and not bf.check(str(order_id)):
        return jsonify({"error": "Order not found"}), 404
    else:    
        order_repo = OrderRepository(db_params)
        order = await order_repo.get_order_by_id(order_id)
        if order:
            return jsonify(order)
        else:
            return jsonify({"error": "Order not found"}), 404
    # return "end"
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Add any other desired parameters
