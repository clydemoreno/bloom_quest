import math

def calculate_bloom_filter_size(n, p):
    m = - (n * math.log(p)) / (math.log(2) ** 2)
    m = math.ceil(m)  # Round up to the nearest integer
    return m

def calculate_number_of_hashes(m, n):
    k = (m / n) * math.log(2)
    return int(k)

# Example usage
expected_elements = 6000
false_positive_prob = 0.01  # 1% false positive probability

bloom_filter_size = calculate_bloom_filter_size(expected_elements, false_positive_prob)
number_of_hashes = calculate_number_of_hashes(bloom_filter_size, expected_elements)

print("Bloom filter size (m):", bloom_filter_size, "bits")
print("Number of hash functions (k):", number_of_hashes)
print(f"Bloom Memory size: {int(bloom_filter_size/8)}")

#6 thousand entries using 
print(f"Hash map Memory size: {(expected_elements * 32 )+ (expected_elements * 4)}")

#can you serialize a hash map into a file and then get the file size?



