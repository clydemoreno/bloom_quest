import sys
import unittest
import aiomysql
from mysql_data_writer import MySqlDataWriter  # Adjust the import path
from data_writer_interface import IDataWriter
import asyncio
# sys.path.append('../../utility')
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
folder_to_concatenate = "utility"  # Replace with the folder name you want to concatenate
folder_path = os.path.join(parent_dir, folder_to_concatenate)
sys.path.append(folder_path)
# Now you can import a module from the "utility" folder
from load_config import load_config


class TestMySqlDataRepository(unittest.IsolatedAsyncioTestCase):  # Change the base class to IsolatedAsyncioTestCase

    async def asyncSetUp(self):
        config_data = load_config()
        # print (config_data)
        self.repository = MySqlDataWriter(config_data)

    async def test_get_all_order_ids(self):
        all_ids = await self.repository.get_all_ids()
        self.assertGreater(len(all_ids), 0)

    async def test_get_record_count(self):
        total_records = await self.repository.get_record_count()
        self.assertGreater(total_records, 0)

    async def test_build_array(self):
        array_length = await self.repository.build_array()
        self.assertGreater(array_length, 0)

if __name__ == '__main__':
    unittest.main()

    
