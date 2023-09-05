import hashlib
import math
import numpy as np
from array import array 
from bloom_filter_array import BloomFilterArray
import sys
sys.path.append("./messaging")

from IAsyncObserver import IAsyncObserver

sys.path.append("./reader")
from read_array_with_timestamp import load_array

def custom_hash(val: str, seed: int) -> int:
    if not isinstance(val, str):
        val = str(val)    

    hash_val = hashlib.sha256(val.encode() + bytes([seed])).hexdigest()
    return int(hash_val, 16)

# def _hash( item, seed):
#     return hash(item + str(seed)) 


class BloomFilter (IAsyncObserver):
    def __init__(self, item_count, prob, hash_function=None):
        self.size = self.get_size(item_count, prob)
        self.hash_count = self.get_hash_count(self.size,item_count)
        self.hash_function = hash_function if hash_function else self.default_hash
        # self.hash_function = self.default_hash
        #switched to fixed np array for faster vectorized operations
        self.bf_array = BloomFilterArray(self.size, initialize_with_ones=False)  # Adjust the size and initialization as needed
    
    async def update(self, message):
        print(f"AsyncConcreteObserverA received message: {message}")

        file_name_pattern = "data"
        # Load the latest array
        latest_loaded_array = load_array(self.temp_dir_path, file_name_pattern)
        print(latest_loaded_array)

    def check(self, value):
        for seed in range(self.hash_count):
            index = self.hash_function(value, seed)
            if not self.bf_array.read(index):
                return False
        return True

    @classmethod
    def get_size(self, n, p):
        '''
        Return the size of bit array(m) to used using
        following formula
        m = -(n * lg(p)) / (lg(2)^2)
        n : int
            number of items expected to be stored in filter
        p : float
            False Positive probability in decimal
        '''
        m = -(n * math.log(p))/(math.log(2)**2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        '''
        Return the hash function(k) to be used using
        following formula
        k = (m/n) * lg(2)

        m : int
            size of bit array
        n : int
            number of items expected to be stored in filter
        '''
        k = (m/n) * math.log(2)
        return int(k)
    #implement the abstract method


# Example usage
# bloom_filter = BloomFilter(100, 3)
# words = ["apple", "banana", "cherry", "date", "elderberry"]

# for word in words:
#     bloom_filter.add(word)

# print(bloom_filter.check("apple"))  # Should return True
# print(bloom_filter.check("grape"))  # Should return False
