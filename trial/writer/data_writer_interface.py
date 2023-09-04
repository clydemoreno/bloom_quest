import abc
import numpy as np
class IDataWriter(abc.ABC):

    def __init__(self, db_params):
        self.db_params = db_params
        self.array = None

    @abc.abstractmethod
    async def select_ids_with_paging(self, page_size, page_number):
        pass

    @abc.abstractmethod
    async def get_all_ids(self):
        pass

    @abc.abstractmethod
    async def get_record_count(self) -> int:
        pass

    @abc.abstractmethod
    async def build_array(self):
        pass
