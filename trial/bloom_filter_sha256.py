import hashlib
import math
import numpy as np
from array import array
from bloom_filter_array import BloomFilterArray
from pathlib import Path
import copy

import sys
# Get the current script's directory
parent_dir = Path(__file__).resolve().parent
# Add the 'messaging' directory to sys.path
sys.path.append(str(parent_dir / 'messaging'))
from IAsyncObserver import IAsyncObserver
from checksum import checksum

# Get the current script's directory
sys.path.append(str(parent_dir / 'reader'))
from read_array_with_timestamp import load_array
from writer.use_proto_buf import load_data_from_file


def custom_hash(val: str, seed: int) -> int:
    if not isinstance(val, str):
        val = str(val)

    hash_val = hashlib.sha256(val.encode() + bytes([seed])).hexdigest()
    return int(hash_val, 16)

class BloomFilter(IAsyncObserver):
    def __init__(self, item_count, prob, hash_function=None):
        self.prob = prob
        self.size = self.get_size(item_count, self.prob)
        self.hash_count = self.get_hash_count(self.size, item_count)
        self.hash_function = hash_function if hash_function else self.default_hash
        self.bf_array = BloomFilterArray(self.size, initialize_with_ones=False)
        

    async def update(self, message):
        print(f"Bloom filter received message: {message}")
        file_name_pattern = "data"
        # latest_loaded_array = load_array(str(parent_dir / 'data'), file_name_pattern)
        # print(latest_loaded_array)

        latest_loaded_array, loaded_hash_count, loaded_array_length = load_data_from_file(str(parent_dir / 'data'), file_name_pattern)
        print("Loaded latest array")
        self.update_array(latest_loaded_array, loaded_hash_count, loaded_array_length)

    def check(self, value):
        for seed in range(self.hash_count):
            index = self.hash_function(value, seed)
            if not self.bf_array.read(index):
                return False
        return True

    def default_hash(self, value, seed):
        return custom_hash(value, seed) % self.size

    def update_array(self, array, hash_count, array_length):
        self.size = array_length

        # fp2 = config_data["bloom_filter"]["false_positive_probability"]
        # size = config_data["bloom_filter"]["size"]

        # Copy over the bitarray from bloomfilter1 to bloomfilter2
        
        self.size = self.get_size(array_length, self.prob)
        self.hash_count = self.get_hash_count(self.size, array_length)
        self.bf_array = BloomFilterArray(self.size, initialize_with_ones=False)
        self.bf_array.array = copy.deepcopy(array)

        print(f"Updated array: {self.hash_count}")
        print(f"Updated size: {self.size}")
        # print("updated checksum", checksum(array.tolist()))


    def add(self, value):
        for seed in range(self.hash_count):
            index = self.hash_function(value, seed)
            self.bf_array.array[index] = 1

    @classmethod
    def get_size(self, n, p):
        # n = size of entries
        # p = prob
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        k = (m / n) * math.log(2)
        return int(k)

if __name__ == "__main__":
    # Testing the BloomFilter class
    bloom_filter = BloomFilter(100, 0.05)  # Adjust item_count and prob as needed
    words = ["apple", "banana", "cherry", "date", "elderberry"]

    for word in words:
        bloom_filter.add(word)

    print(bloom_filter.check("apple"))  # Should return True
    print(bloom_filter.check("grape"))  # Should return False


    bloom_filter.add("201")
    print(bloom_filter.check("201"))  # Should return True
    
