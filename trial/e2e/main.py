import asyncio
import psutil

from pathlib import Path
import sys

# Adjust the path to the parent directory containing the utility folder
sys_path = Path(__file__).resolve().parent.parent
sys_path_str = str(sys_path)
if sys_path_str not in sys.path:
    sys.path.append(sys_path_str)


# Import your required modules from the utility and other sources
from utility.load_config import load_config
from writer.mysql_data_writer import MySqlDataWriter
from writer.data_writer_interface import IDataWriter
from reader.bloom_filter_reader import BloomFilterReader
from writer.validate_array import validate_array

# Import the PeriodicTask from your app.py
from web.periodic_task import PeriodicTask

from bloom_filter_sha256 import BloomFilter


# Start monitoring memory usage before running the script
process = psutil.Process()
start_memory_usage = process.memory_info().rss / 1024  # in KB



async def do_something(repository: IDataWriter):
    await repository.build_array()
    print("Async build array completed. IDs:")
    # Calculate memory usage after running the script
    end_memory_usage = process.memory_info().rss / 1024  # in KB
    memory_usage_diff = end_memory_usage - start_memory_usage
    print(f"Memory used by the script: {memory_usage_diff} KB")

async def validate_something(repository: IDataWriter, bf):
    print("Async validation task completed. IDs:")
    # Calculate memory usage after running the script
    end_memory_usage = process.memory_info().rss / 1024  # in KB
    memory_usage_diff = end_memory_usage - start_memory_usage
    if bf is not None:
        print(f"bf check int: {bf.check(201)}")
        print(f"bf check str: {bf.check(str(201))}")
    validate_array(await repository.get_all_ids(), bf, False)
    print(f"Memory used by the script: {memory_usage_diff} KB")

async def main():

    # Example usage:
    def my_callback(message):
        print("my callback got called")
        if br_subject is not None:
            asyncio.run(br_subject.notify(f"Event callback executed. {message}"))

    config_data = load_config()
    writer = MySqlDataWriter(config_data)
    await asyncio.sleep(2)  # Sleep for 2 seconds to write the data
    size = config_data["bloom_filter"]["size"]
    fp = config_data["bloom_filter"]["false_positive_probability"]
    bf_observer = BloomFilter(size, fp)
    print(f"Initial size: {bf_observer.size}, Initial hash count: {bf_observer.hash_count}")
    folder_path = str(sys_path / config_data["data"]["path"])
    print("folder to watch: ", folder_path)
    br_subject = BloomFilterReader(folder_path)
    await br_subject.attach(bf_observer)

    # Create a PeriodicTask instance with your callback
    periodic_task = PeriodicTask(my_callback, interval_seconds=30)

    try:

        await do_something(writer)
        await asyncio.sleep(3)  # Sleep for 10 seconds using asyncio.sleep
        await validate_something(writer, bf_observer)
        while True:
            await do_something(writer)
            await asyncio.sleep(60)  # Sleep for 10 seconds using asyncio.sleep
            await validate_something(writer, bf_observer)
    except KeyboardInterrupt:
        print("Stopped")
        br_subject.file_listener.stop()

        # Calculate memory usage after running the script
        end_memory_usage = process.memory_info().rss / 1024  # in KB
        memory_usage_diff = end_memory_usage - start_memory_usage
        print(f"Memory used by the script: {memory_usage_diff} KB")

    # Stop the periodic task when the script exits
    periodic_task.stop()
    periodic_task.join()

if __name__ == "__main__":
    asyncio.run(main())
