import random
import math
from array import array
class BloomFilter:
    def __init__(self, size, prob):
        self.size = self.calculate_size(size, prob)
        # switch to a fixed size array to reduce memory footprint
        # 'b' is the typecode for signed char (which is used to represent boolean values)
        self.bit_array =  array('b',[False] * self.size)  
        self.num_hash_functions = self.calculate_number_of_hashes(self.size, size)
        
    def _hash(self, item, seed):
        return hash(item + str(seed)) % self.size
    
    def insert(self, item):
        for i in range(self.num_hash_functions):
            index = self._hash(item, i)
            self.bit_array[index] = True
            
    def query(self, item):
        for i in range(self.num_hash_functions):
            index = self._hash(item, i)
            if not self.bit_array[index]:
                return False
        return True
    
    def calculate_size(self, n, p):
        m = - (n * math.log(p)) / (math.log(2) ** 2)
        m = math.ceil(m)
        return m
    
    def calculate_number_of_hashes(self, m, n):
        k = (n / m) * math.log(2)
        return int(k)





def simulate_bloom_filter(expected_elements, false_positive_prob, num_trials):
    bloom_filter = BloomFilter(expected_elements, false_positive_prob)
    
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    for _ in range(num_trials):
        # Generate random data items
        true_elements = [str(random.randint(1, 10000)) for _ in range(expected_elements)]
        false_elements = [str(random.randint(10001, 20000)) for _ in range(expected_elements)]
        query_elements = true_elements + false_elements
        # Insert true elements into the Bloom filter
        for element in true_elements:
            bloom_filter.insert(element)
            
        # Check false positive rate
        # for element in query_elements:
        #     if not bloom_filter.query(element):
        #         if element not in true_elements:
        #             true_negatives += 1
        #     else:
        #         if element not in true_elements:
        #             false_positives += 1


        for item in query_elements:
            if not bloom_filter.query(item):
                if item in true_elements:
                    false_negatives += 1

            else:
                if item not in true_elements:
                    false_positives += 1
                    


    
    # print(f"Expected True negatives: {true_negatives} count: {len(false_elements)}")

    observed_false_positive_prob = false_positives / (num_trials * expected_elements)
    return observed_false_positive_prob


# Simulation parameters
expected_elements = 1000
false_positive_prob = 0.01  # 1% false positive probability
num_trials = 100

observed_false_positive_prob = simulate_bloom_filter(expected_elements, false_positive_prob, num_trials)


print(f"Expected False Positive Probability: {false_positive_prob}")
print(f"Observed False Positive Probability: {observed_false_positive_prob}")
