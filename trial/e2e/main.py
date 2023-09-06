import time
import asyncio
from mysql_data_writer import MySqlDataWriter
from load_config import load_config

async def do_something(repository):
    ids = await repository.build_array()
    print("Async task completed. IDs:", ids)

def main():
    config_data = load_config()
    repository = MySqlDataWriter(config_data)

    try:
        while True:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(do_something(repository))
            time.sleep(10)  # Sleep for 5 minutes (300 seconds)
    except KeyboardInterrupt:
        print("Stopped")

if __name__ == "__main__":
    main()
