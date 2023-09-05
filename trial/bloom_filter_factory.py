import hashlib
import math
from array import array
from bloom_filter_sha256 import BloomFilter 
from bloom_filter_interface import IBloomFilter

class BloomFilterFactory:
    @staticmethod
    def create_from_config(config) -> IBloomFilter:
        bloom_filter_config = config.get("bloom_filter", {})
        item_count = bloom_filter_config.get("size", 30)
        probability = bloom_filter_config.get("false_positive_probability", 0.05)
        return IBloomFilter(BloomFilter(item_count, probability))


# # Example usage:
# config_loader = AsyncConfigLoader('../async/config.json')
# config_data = await config_loader.load_config_async()

# bloom_filter = BloomFilterFactory.create_from_config(config_data)
# words = ["apple", "banana", "cherry", "date", "elderberry"]

# for word in words:
#     bloom_filter.add(word)

# print(bloom_filter.check("apple"))  # Should return True
# print(bloom_filter.check("grape"))  # Should return False
