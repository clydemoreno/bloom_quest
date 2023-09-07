import hashlib
import math
import numpy as np
from array import array 
from bloom_filter_array import BloomFilterArray
from pathlib import Path

import sys
# Get the current script's directory
parent_dir = Path(__file__).resolve().parent
# Add the 'messaging' directory to sys.path
sys.path.append(str(parent_dir / 'messaging'))
from IAsyncObserver import IAsyncObserver


# Get the current script's directory
sys.path.append(str(parent_dir / 'reader'))
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
        print(f"Bloom filter received message: {message}")
        file_name_pattern = "data"
        # Load the latest array
        latest_loaded_array = load_array(str(parent_dir / 'data') , file_name_pattern)
        print(latest_loaded_array)
        #need to do validation
        self.update_array(latest_loaded_array)
        

    def check(self, value):
        for seed in range(self.hash_count):
            index = self.hash_function(value, seed)
            if not self.bf_array.read(index):
                return False
        return True

    def default_hash(self, value, seed):
        return custom_hash(value, seed) % self.size
        

    def update_array(self, value):
        self.bf_array.write(value)

    def add(self, value):
        for seed in range(self.hash_count):
            index = self.hash_function(value, seed)
            self.bf_array.array[index] = 1


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
