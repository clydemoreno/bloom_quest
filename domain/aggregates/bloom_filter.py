import math

class BloomFilter:
    def __init__(self, size, num_hash_functions):
        self.size = size
        self.bit_array = [0] * size
        self.num_hash_functions = num_hash_functions
        
    def _murmurhash(self, data, seed):
        m = 0x5bd1e995
        r = 24
        
        h = seed ^ len(data)
        while len(data) >= 4:
            k = int.from_bytes(data[:4], byteorder='little')
            k *= m
            k ^= (k >> r)
            k *= m
            h *= m
            h ^= k
            data = data[4:]
            
        if len(data) > 0:
            h ^= int.from_bytes(data, byteorder='little')
            h *= m
        
        h ^= (h >> 13)
        h *= m
        h ^= (h >> 15)
        
        return h % self.size
    
    def insert(self, item):
        for i in range(self.num_hash_functions):
            index = self._murmurhash(item.encode(), i)
            self.bit_array[index] = 1
            
    def query(self, item):
        for i in range(self.num_hash_functions):
            index = self._murmurhash(item.encode(), i)
            if self.bit_array[index] == 0:
                return False
        return True

# Calculating Bloom filter size and number of hash functions
def calculate_bloom_filter_size(n, p):
    m = - (n * math.log(p)) / (math.log(2) ** 2)
    m = math.ceil(m)
    return m

def calculate_number_of_hashes(m, n):
    k = (m / n) * math.log(2)
    return int(k)



