import sys
import aiomysql
import abc
import asyncio
import random
from datetime import datetime
import numpy as np
from pathlib import Path  # Import pathlib.Path for path handling
import os
# Append the parent directory to the sys.path if necessary
sys.path.append(str(Path(__file__).resolve().parent.parent / "db"))  # Adjust the path as needed
from order_repository import OrderRepository


# Append the parent directory to the sys.path if necessary
sys.path.append(str(Path(__file__).resolve().parent.parent))
from bloom_filter_sha256 import BloomFilter

# Import your custom utility functions/modules with pathlib
sys.path.append(str(Path(__file__).resolve().parent))

from save_array_with_timestamp import save_array_with_timestamp
from cleanup_old_files import cleanup_old_files

from data_writer_interface import IDataWriter

from validate_array import validate_array

from bf_data_pb2 import CustomData 

from use_proto_buf import save_data_to_file, load_data_from_file


# folder_path = os.path.join(parent_dir, folder_to_concatenate)
# sys.path.append(folder_path)
# Now you can import a module from the "utility" folder
# Add the 'messaging' directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / "utility"))  # Adjust the path as needed

from load_config import load_config



from checksum import checksum

class MySqlDataWriter(IDataWriter):
    def __init__(self, config_data):
        self.db_params = config_data["database"]
        self.data = config_data["data"]
        self.bloom_filter_parameters = config_data["bloom_filter"]

    async def select_ids_with_paging(self, page_size, page_number):
        return [10, 2]

    async def get_all_ids(self):
        order_repository = OrderRepository(self.db_params)
        all_ids = await order_repository.get_all_orders()
        return all_ids

    async def get_record_count(self) -> int:
        order_repository = OrderRepository(self.db_params)
        all_ids = await order_repository.count_records()
        return all_ids



    async def build_array(self):
        # Implement your logic to build the array here
        self.ids = await self.get_all_ids()

        bloom_filter = BloomFilter(len(self.ids), self.bloom_filter_parameters["false_positive_probability"])
        print(f"Bloom filter hash count: {bloom_filter.hash_count}")
        print(f"Bloom filter bit size: {bloom_filter.size}")

        for item in self.ids:
            bloom_filter.add(item['ID'])

        validate_array(self.ids, bloom_filter, initial=True)

        # Create a NumPy array from the Bloom filter
        # my_
        # array = np.array([bloom_filter.bf_array.array, checksum(bloom_filter.bf_array.array.tolist()), bloom_filter.hash_count])
        cs = checksum(bloom_filter.bf_array.array.tolist())
        my_array = bloom_filter.bf_array.array
        # Specify the directory and file nxame using pathlib.Path
        parent_dir = Path(__file__).resolve().parent.parent
        save_directory = parent_dir / self.data["path"]
        file_name = self.data['file_name']

        # save_array_with_timestamp(my_array, save_directory, file_name)

        # Save data to a protobuf file
        save_data_to_file(
            my_array.tolist(), bloom_filter.hash_count, len(self.ids), save_directory, file_name
        )

        cleanup_old_files(save_directory)

        return len(my_array)




