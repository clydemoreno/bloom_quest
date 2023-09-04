from data_writer_interface import IDataWriter
import aiomysql
import abc
import sys
sys.path.append('../db/')
from order_repository import OrderRepository

class MySqlDataWriter(IDataWriter):
    def __init__(self, config_data):
        self.db_params = config_data["database"]

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
        pass

