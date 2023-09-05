from data_writer_interface import IDataWriter
import aiomysql
import abc
import sys
from datetime import datetime

sys.path.append('../db/')
from order_repository import OrderRepository

sys.path.append('../')
from bloom_filter_sha256 import BloomFilter

import numpy as np
from pathlib import Path

from save_array_with_timestamp import save_array_with_timestamp
from cleanup_old_files import cleanup_old_files

class MySqlDataWriter(IDataWriter):
    def __init__(self, config_data):
        self.db_params = config_data["database"]
        self.data = config_data["data"]

    async def select_ids_with_paging(self, page_size, page_number):
        return [10,2]
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
        
        ids = await self.get_all_ids()
        bloom_filter = BloomFilter(len(ids), 0.05)
        for item in ids:
            bloom_filter.add(item)
        




        # Create a NumPy array (example)
        my_array = bloom_filter.bf_array.array

        # Specify the directory and file name
        save_directory = Path(self.data["path"])
        file_name = self.data['file_name']

        save_array_with_timestamp(my_array, save_directory, file_name)

        cleanup_old_files(save_directory)

        # # Get the current timestamp
        # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # # Append the timestamp to the original file name
        # file_name_with_timestamp = f"{file_name}_{timestamp}.npy"

        # # Create the full path by joining the directory and file name
        # save_path = save_directory / file_name_with_timestamp

        # # Save the array to the specified path
        # np.save(save_path, my_array)


        
