# test_bloom_filter.py
import unittest
import asyncio
import sys
from pathlib import Path
sys.path.append('./async')

# from async_config_loader import AsyncConfigLoader

from bloom_filter_factory import BloomFilterFactory
# from async_config_loader import AsyncConfigLoader

parent_dir = Path(__file__).resolve().parent
# Add the 'messaging' directory to sys.path
sys.path.append(str(parent_dir / 'utility'))
from load_config import load_config




class TestBloomFilter(unittest.TestCase):
    async def asyncSetUp(self):
        pass
        # Load configuration data asynchronously
        # config_loader = AsyncConfigLoader('./async/config.json')
        # self.config_data = await config_loader.load_config_async()
        self.config_data = load_config
    
    def test_bloom_filter(self):
        # Ensure that the asyncSetUp method has completed before creating the BloomFilter
        # asyncio.run(self.asyncSetUp())

        # # Create a BloomFilter instance using the factory
        bloom_filter = BloomFilterFactory.create_from_config(self.config_data)

        # Test the BloomFilter with integer data
        # data = [1, 2, 3, 4, 5]  # Replace with your integer data
        # for item in data:
        #     bloom_filter.add(item)
        words = ["apple", "banana", "cherry", "date", "elderberry"]

        for word in words:
            bloom_filter.add(word)

        # # Check if the integers are in the BloomFilter
        self.assertTrue(bloom_filter.check("apple"))  # Should return True
        self.assertTrue(bloom_filter.check("orange") != True)  # Should return False


