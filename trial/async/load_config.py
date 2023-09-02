import json
from async_file import AsyncFile  # Import your AsyncFile class

async def load_config_async():
    async with AsyncFile('config.json', 'r') as json_file:
        content = await json_file.read()
        config_data = json.load(content)
    return config_data
