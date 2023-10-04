import asyncio
import psutil
from pathlib import Path
import sys
import copy 
import numpy as np

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
from bloom_filter_sha256 import BloomFilter
from bloom_filter_array import BloomFilterArray

# Start monitoring memory usage before running the script
process = psutil.Process()
start_memory_usage = process.memory_info().rss / 1024  # in KB


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

    # Load configuration data
    config_data = load_config()

    # Create an order repository to get all IDs
    order_repository = MySqlDataWriter(config_data)
    ids = await order_repository.get_all_ids()

    # Instantiate the first BloomFilter with the size based on the number of IDs
    size1 = len(ids)
    fp1 = config_data["bloom_filter"]["false_positive_probability"]
    bf1 = BloomFilter(size1, fp1)


    # Populate the bitarray of bloomfilter1 using the IDs
    for item in ids:
        bf1.add(item['ID'])

    # Validate bloomfilter1
    await validate_something(order_repository, bf1)

    # Instantiate the second BloomFilter with the size based on the number of IDs
    # size2 = len(ids)
    fp2 = config_data["bloom_filter"]["false_positive_probability"]
    size = config_data["bloom_filter"]["size"]
    bf2 = BloomFilter(size, fp2)

    # Copy over the bitarray from bloomfilter1 to bloomfilter2
    
    bf2.size = bf1.get_size(size1, fp1)
    bf2.hash_count = bf1.get_hash_count(bf2.size, size1)
    bf2.bf_array = BloomFilterArray(bf2.size, initialize_with_ones=False)
    bf2.bf_array.array = copy.deepcopy(bf1.bf_array.array)
    
    are_identical = np.array_equal(bf1.bf_array.array, bf2.bf_array.array)

    # Compare the two BloomFilters
    if bf1.size == bf2.size and bf1.hash_count == bf2.hash_count and are_identical:
        print(f"BloomFilters 1 and 2 are identical: {are_identical} in terms of size1 {bf1.size}: size2 {bf2.size}, hash count, and false positive probability.")

    print(f"identical: {are_identical} in terms of bf1 size {bf1.size}: bf2 size {bf2.size}, bf hash count 1: {bf1.hash_count} bf 2 hash count: {bf2.hash_count}.")
    # Validate bloomfilter2
    await validate_something(order_repository, bf2)
    print("validate again")
    # Validate bloomfilter2
    await validate_something(order_repository, bf1)

if __name__ == "__main__":
    asyncio.run(main())
