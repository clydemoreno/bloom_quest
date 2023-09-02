import asyncio
import unittest
import sys
sys.path.append('../async/')

from async_file import AsyncFile  # Import your AsyncFile class
from async_config_loader import AsyncConfigLoader


from bloom_filter_factory import BloomFilterFactory
from async_config_loader import AsyncConfigLoader

async def my_func():
    await asyncio.sleep(0.1)
    return True

class TestStuff(unittest.IsolatedAsyncioTestCase):
    async def test_my_func(self):
        r = await my_func()
        self.assertTrue(r)