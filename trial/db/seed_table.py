import asyncio
from order_repository import OrderRepository
from async_config_loader import AsyncConfigLoader  # Import your AsyncConfigLoader class

# Generate random test data
def generate_test_data(num_rows):
    data = []
    for i in range(1, num_rows + 1):
        order_id = i
        order_name = f"Order_{i}"
        data.append((order_id, order_name))
    return data

# Number of rows in the table
num_rows = 5000

# Generate test data
test_data = generate_test_data(num_rows)

async def main():
    config_loader = AsyncConfigLoader('config.json')
    config_data = await config_loader.load_config_async()
    db_params = config_data['database']
    
    order_repository = OrderRepository(db_params)
    await order_repository.insert_orders(test_data)
    print("Data inserted successfully")

if __name__ == "__main__":
    asyncio.run(main())
