import asyncio
from async_config_loader import AsyncConfigLoader

async def main():
    config_loader = AsyncConfigLoader('config.json')
    config_data = await config_loader.load_config_async()
    db_host = config_data['database']['host']
    print(f"db host: {db_host}")
    # Use db_host and other configuration values

if __name__ == "__main__":
    asyncio.run(main())
