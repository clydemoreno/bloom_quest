import time
import asyncio
from pathlib import Path
import sys
# Adjust the path to the parent directory containing the utility folder
sys_path = Path(__file__).resolve().parent.parent
sys_path_str = str(sys_path)
if sys_path_str not in sys.path:
    sys.path.append(sys_path_str)

from utility.load_config import load_config  # Import load_config from the utility folder
from writer.mysql_data_writer import MySqlDataWriter
from writer.data_writer_interface import IDataWriter

# parent_dir = Path(__file__).resolve().parent
# parent_dir_str = str(parent_dir)
# if parent_dir_str not in sys.path:
#     sys.path.append(parent_dir_str)


from bloom_filter_sha256 import BloomFilter



async def do_something(repository:IDataWriter):
    ids = await repository.build_array()
    print("Async task completed. IDs:", ids)

def main():
    config_data = load_config()
    repository = MySqlDataWriter(config_data)
    size = config_data["bloom_filter"]["size"]
    fp = config_data["bloom_filter"]["false_positive_probability"]
    bf = BloomFilter(size,fp)




    try:
        while True:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(do_something(repository))
            time.sleep(10)  # Sleep for 10 seconds
    except KeyboardInterrupt:
        print("Stopped")

if __name__ == "__main__":
    main()
