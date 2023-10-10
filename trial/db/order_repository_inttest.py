import asyncio
from order_repository import OrderRepository
from pathlib import Path
import sys

# Adjust the path to the parent directory containing the utility folder
sys_path = Path(__file__).resolve().parent.parent
sys_path_str = str(sys_path)
if sys_path_str not in sys.path:
    sys.path.append(sys_path_str)


# Import your required modules from the utility and other sources
from utility.load_config import load_config



# sys.path.append('../async/')
# from async_config_loader import AsyncConfigLoader


import test_data_generator
async def generate_entries():
    # config_loader = AsyncConfigLoader('../async/config.json')

    # config_data = await config_loader.load_config_async()
    config_data = load_config()
    db_params = config_data['database']
    order_repository = OrderRepository(db_params)
    # Generate test data
    num_rows = 100
    test_data = test_data_generator.generate_test_data(num_rows)
    await order_repository.insert_orders(test_data)
    print("Data inserted successfully")

async def test_get_order_by_id(order_id):
    # config_loader = AsyncConfigLoader('../async/config.json')
    # config_data = await config_loader.load_config_async()
    config_data = load_config()
    db_params = config_data['database']
    
    order_repository = OrderRepository(db_params)

    try:
        order = await order_repository.get_order_by_id(order_id)
        if order:
            print(f"Order ID: {order['ID']}, Order Name: {order['Name']}")
        else:
            print("Order not found")
    except Exception as e:
        print("An error occurred:", e)

async def select():
    # config_loader = AsyncConfigLoader('../async/config.json')
    # config_data = await config_loader.load_config_async()
    config_data = load_config()
    db_params = config_data['database']
    order_repository = OrderRepository(db_params)

    # Calculate total records and pages
    total_records = await order_repository.count_records()
    page_size = 10
    total_pages = (total_records + page_size - 1) // page_size

    # Select orders with paging using a for loop
    for page_number in range(1, total_pages + 1):
        orders = await order_repository.select_orders_with_paging(page_size, page_number)
        print(f"Page {page_number} Orders:")
        for order in orders:
            print(f"Order ID: {order['ID']}, Order Name: {order['Name']}")

if __name__ == "__main__":
    try:
        asyncio.run(select())
        asyncio.run(generate_entries())
        asyncio.run(select())
        asyncio.run(test_get_order_by_id(5))
    except Exception as e:
        print("An error occurred:", e)
