import hashlib
import math
from array import array 

MAX_ENTRIES = 10  # Maximum number of entries allowed
class BloomFilter:
    def __init__(self, item_count, prob):
        self.size = self.get_size(item_count, prob)
        self.hash_count = self.get_hash_count(self.size, item_count)
        self.entries = [(0, array('b', [False] * self.size))]

    def _hash(self, value, seed):
        hash_val = hashlib.sha256(value.encode() + bytes([seed])).hexdigest()
        return int(hash_val, 16) % self.size

    def add_entry(self, value, timestamp):
        new_bit_array = self._create_new_bit_array(value)
        self.entries.append((timestamp, new_bit_array))
        self._limit_entries()

    def check(self, value):
        latest_bit_array = self._get_latest_bit_array()
        if latest_bit_array:
            for seed in range(self.hash_count):
                index = self._hash(value, seed)
                if not latest_bit_array[index]:
                    return False
            return True
        return False

    def _get_latest_bit_array(self):
        if self.entries:
            latest_entry = max(self.entries, key=lambda entry: entry[0])
            return latest_entry[1]
        return None

    def _create_new_bit_array(self, value):
        new_bit_array = array('b', [False] * self.size)
        for seed in range(self.hash_count):
            index = self._hash(value, seed)
            new_bit_array[index] = True
        return new_bit_array

    def _limit_entries(self):
        if len(self.entries) > MAX_ENTRIES:
            self.entries = self.entries[-MAX_ENTRIES:]


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
