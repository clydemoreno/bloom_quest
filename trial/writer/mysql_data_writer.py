import sys
import aiomysql
import abc
import random
from datetime import datetime
import numpy as np
from pathlib import Path  # Import pathlib.Path for path handling

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
        for item in self.ids:
            bloom_filter.add(item)

        # Create a NumPy array (example)
        my_array = bloom_filter.bf_array.array

        # Specify the directory and file name using pathlib.Path
        parent_dir = Path(__file__).resolve().parent.parent
        save_directory = parent_dir / self.data["path"]

        file_name = self.data['file_name']

        save_array_with_timestamp(my_array, save_directory, file_name)

        cleanup_old_files(save_directory)
        
        return len(my_array)

    async def validate_bloom_filter_array(self, bf: BloomFilter):
        false_elements = [str(random.randint(1001, 2000)) for _ in range(len(bf.bf_array.array)) ]
        false_negatives = 0
        false_positives = 1

        for item in self.ids:
            if not bf.check(item):
                false_negatives += 1

        for item in false_elements:
            if bf.check(item + "pre_"): #this makes it unique and not in the true elements
                false_positives += 1
        false_positive_ratio = false_positives / (len(self.ids ) + len(bf.bf_array.array))
        false_negatives_ratio = false_negatives / (len(self.ids ) + len(bf.bf_array.array))
        print(f"false positives ratio: {false_positive_ratio}")
        print(f"false negatives ratio: {false_negatives_ratio}")


