from bloom_filter_geek import BloomFilter
from random import shuffle
import random
from bloom_filter_sha256 import BloomFilter as BloomFilterSha256
from bloom_filter_interface import IBloomFilter
n = 20 #no of items to add
p = 0.05 #false positive probability

bloomf = IBloomFilter( BloomFilterSha256(n,p))
print("Size of bit array:{}".format(bloomf.size))
print("False positive Probability:{}".format(bloomf.fp_prob))
print("Number of hash functions:{}".format(bloomf.hash_count))

# words to be added
word_present = ['abound','abounds','abundance','abundant','accessible',
				'bloom','blossom','bolster','bonny','bonus','bonuses',
				'coherent','cohesive','colorful','comely','comfort',
				'gems','generosity','generous','generously','genial']

# word not added
word_absent = ['bluff','cheater','hate','war','humanity',
			'racism','hurt','nuke','gloomy','facebook',
			'geeksforgeeks','twitter']

for item in word_present:
	bloomf.add(item)

shuffle(word_present)
shuffle(word_absent)

test_words = word_present[:10] + word_absent
shuffle(test_words)

for word in test_words:
	if bloomf.check(word):
		if word in word_absent:
			print("'{}' is a false positive!".format(word))
		else:
			print("'{}' is probably present!".format(word))
	else:
		print("'{}' is definitely not present!".format(word))



def simulate_bloom_filter(expected_elements, false_positive_prob, num_trials):
    
    bloom_filter = BloomFilter(expected_elements,false_positive_prob)

    print("Size of bit array:{}".format(bloom_filter.size))
    print("False positive Probability:{}".format(bloom_filter.fp_prob))
    print("Number of hash functions:{}".format(bloom_filter.hash_count))

    false_positives = 0
    true_negatives = 0
    true_positives = 0
    false_negatives = 0
    for _ in range(num_trials):
        # Generate random data items
        true_elements = [str(random.randint(1, 10000)) for _ in range(expected_elements ) ]
        false_elements = [str(random.randint(20000, 30000)) for _ in range(expected_elements) ]
        query_elements = true_elements + false_elements
        # query_elements.append(true_elements)
        # query_elements.append(false_elements)

        # Insert true elements into the Bloom filter
        for element in true_elements:
            bloom_filter.add(element)
            


        # Check false positive rate and true negatives
        for element in query_elements:
            if not bloom_filter.check(element):
                if element in false_elements:
                    true_negatives += 1
                else:
                    false_negatives += 1
            else:
                if element in true_elements:
                    true_positives += 1
                else:
                    true_negatives += 1


    print("true negatives", true_negatives, len(true_elements), len(false_elements), len(query_elements))

    observed_false_positive_prob = false_positives / (num_trials * expected_elements)
    observed_true_negative_prob = true_negatives / (num_trials * expected_elements)
    observed_true_positive_prob = true_positives / (num_trials * expected_elements)
    observed_false_negative_prob = false_negatives / (num_trials * expected_elements)
    return observed_false_positive_prob,observed_true_negative_prob, observed_true_positive_prob, observed_false_negative_prob

# # Simulation parameters
# expected_elements = 1000
# false_positive_prob = 0.05  # 1% false positive probability
# num_trials = 500

# observed_false_positive_prob, observed_true_negative_prob,observed_true_positive_prob, observed_false_negative_prob = simulate_bloom_filter(expected_elements, false_positive_prob, num_trials)


# print(f"Expected False Positive Probability: {false_positive_prob}")
# print(f"Observed False Positive Probability: {observed_false_positive_prob}")
# print(f"Observed True Negative Probability: {observed_true_negative_prob}")
# print(f"Observed True Positive Probability: {observed_true_positive_prob}")
# print(f"Observed False Negative Probability: {observed_false_negative_prob}")
