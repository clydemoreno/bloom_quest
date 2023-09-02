import json
import asyncio
from async_file import AsyncFile  # Import your AsyncFile class

class AsyncConfigLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    async def load_config_async(self):
        async with AsyncFile(self.file_path, 'r') as json_file:
            content = await json_file.read()
            config_data = json.loads(content)
        return config_data

# async def main():
#     config_loader = AsyncConfigLoader('config.json')
#     config_data = await config_loader.load_config_async()
#     db_host = config_data['database']['host']
#     print(f"db host:{db_host}")
#     # Use db_host and other configuration values

# if __name__ == "__main__":
#     asyncio.run(main())
