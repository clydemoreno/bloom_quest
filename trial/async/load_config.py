import json
from async_file import AsyncFile
from pathlib import Path  # Import pathlib for working with paths

async def load_config_async():
    config_file_path = Path(__file__).resolve().parent / 'config.json'

    async with AsyncFile(config_file_path, 'r') as json_file:
        content = await json_file.read()
        config_data = json.loads(content)
    return config_data
