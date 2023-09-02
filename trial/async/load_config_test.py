from load_config import load_config_async
import asyncio

async def main():
    config_data = await load_config_async()
    # db_host = config_data['database']['host']
    # Use db_host and other configuration values

if __name__ == "__main__":
    asyncio.run(main())
