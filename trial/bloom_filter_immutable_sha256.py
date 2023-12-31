import hashlib
import math
# from array import array 
from bloom_filter_array import BloomFilterArray
import sys
sys.path.append("./messaging")
from IAsyncObserver import IAsyncObserver

MAX_ENTRIES = 10  # Maximum number of entries allowed
class BloomFilter (IAsyncObserver):
    def __init__(self, item_count, prob):
        self.size = self.get_size(item_count, prob)
        self.hash_count = self.get_hash_count(self.size, item_count)
        self.bf_array = BloomFilterArray(self.size, initialize_with_ones=False)  # Adjust the size and initialization as needed

    def _hash(self, value, seed):
        hash_val = hashlib.sha256(value.encode() + bytes([seed])).hexdigest()
        return int(hash_val, 16) % self.size

    def add_entry(self, value):
        self.bf_array.write(value)

    def check(self, value):
        
        for seed in range(self.hash_count):
            index = self._hash(value, seed)
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
    async def update(self, message):
        print(f"Received message: {message}")



# Example usage
# bloom_filter = BloomFilter(100, 3)
# words = ["apple", "banana", "cherry", "date", "elderberry"]

# for word in words:
#     bloom_filter.add(word)

# print(bloom_filter.check("apple"))  # Should return True
# print(bloom_filter.check("grape"))  # Should return False
