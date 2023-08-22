import random
import math

class BloomFilter:
    def __init__(self, size, num_hash_functions):
        self.size = size
        self.bit_array = [False] * size
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
            self.bit_array[index] = True
            
    def query(self, item):
        for i in range(self.num_hash_functions):
            index = self._murmurhash(item.encode(), i)
            if not self.bit_array[index]:
                return False
        return True

def simulate_bloom_filter(expected_elements, false_positive_prob, num_trials):
    size = calculate_bloom_filter_size(expected_elements, false_positive_prob)
    num_hash_functions = calculate_number_of_hashes(size, expected_elements)
    bloom_filter = BloomFilter(size, num_hash_functions)
    
    false_positives = 0
    true_negatives = 0
    for _ in range(num_trials):
        # Generate random data items
        true_elements = set([str(random.randint(1, 10000)) for _ in range(expected_elements)])
        query_elements = [str(random.randint(10001, 20000)) for _ in range(expected_elements)]
        
        # Insert true elements into the Bloom filter
        for element in true_elements:
            bloom_filter.insert(element)
            

        # Check false positive rate and true negatives
        for element in query_elements:
            if bloom_filter.query(element):
                if element in true_elements:
                    true_positives += 1
                else:
                    false_positives += 1
            else:
                true_negatives += 1

    
    observed_false_positive_prob = false_positives / (num_trials * expected_elements)
    observed_true_negative_rate = true_negatives / (num_trials * expected_elements)
    return observed_false_positive_prob, observed_true_negative_rate

# Calculating Bloom filter size and number of hash functions
def calculate_bloom_filter_size(n, p):
    m = - (n * math.log(p)) / (math.log(2) ** 2)
    m = math.ceil(m)
    return m

def calculate_number_of_hashes(m, n):
    k = (m / n) * math.log(2)
    return int(k)

# Simulation parameters
expected_elements = 1000
false_positive_prob = 0.01  # 1% false positive probability
num_trials = 1000

observed_false_positive_prob, observed_true_negative_rate = simulate_bloom_filter(
    expected_elements, false_positive_prob, num_trials
)

print(f"Expected False Positive Probability: {false_positive_prob}")
print(f"Observed False Positive Probability: {observed_false_positive_prob}")
print(f"Observed True Negative Rate: {observed_true_negative_rate}")
