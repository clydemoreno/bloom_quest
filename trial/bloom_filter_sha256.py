import hashlib
import math
from array import array 
from bloom_filter_array import BloomFilterArray

def custom_hash(val, seed):
    hash_val = hashlib.sha256(val.encode() + bytes([seed])).hexdigest() 
    return int(hash_val, 16)

class BloomFilter:
    def __init__(self, item_count, prob, hash_function=None):
        self.size = self.get_size(item_count, prob)
        self.hash_count = self.get_hash_count(self.size,item_count)
        self.hash_function = hash_function if hash_function else self.default_hash
        # self.hash_function = self.default_hash
        #switched to fixed np array for faster vectorized operations
        self.bf_array = BloomFilterArray(self.size, initialize_with_ones=False)  # Adjust the size and initialization as needed
    
    
    def default_hash(self, value, seed):        
        return custom_hash(value,seed) % self.size
        # return hash_value

    def update_array(self, value):
        self.bf_array.write(value)
    
    def add(self, value):
        for seed in range(self.hash_count):
            index = self.hash_function(value, seed)
            self.bf_array.array[index] = True

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

# Example usage
# bloom_filter = BloomFilter(100, 3)
# words = ["apple", "banana", "cherry", "date", "elderberry"]

# for word in words:
#     bloom_filter.add(word)

# print(bloom_filter.check("apple"))  # Should return True
# print(bloom_filter.check("grape"))  # Should return False
