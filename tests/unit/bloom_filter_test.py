import sys
sys.path.append('../../domain/aggregates')
import random
import bloom_filter as bf


def simulate_bloom_filter(expected_elements, false_positive_prob, num_trials):
    size = bf.calculate_bloom_filter_size(expected_elements, false_positive_prob)
    num_hash_functions = bf.calculate_number_of_hashes(size, expected_elements)
    bloom_filter = bf.BloomFilter(size, num_hash_functions)
    
    false_positives = 0
    true_negatives = 0
    true_positives = 0
    false_negatives = 0
    for _ in range(num_trials):
        # Generate random data items
        true_elements = set([str(random.randint(1, 20)) for _ in range(expected_elements)])
        false_elements = set([str(random.randint(21, 2000)) for _ in range(expected_elements)])
        query_elements = true_elements | false_elements

        print(true_elements)
        print(false_elements)
        # query_elements.append(true_elements )
        # query_elements.append(false_elements )

        # for val in query_elements:
        #     print("first item in query elements", val)
        #     break        
        
        # Insert true elements into the Bloom filter
        for element in true_elements:
            bloom_filter.insert(element)

        for element in true_elements:
            if bloom_filter.query(element):
                true_positives += 1
        
        for element in false_elements:
            if not bloom_filter.query(element):
                true_negatives += 1
            else:
                false_negatives += 1


        # check true negatives

        # Check false positive rate and true negatives
        # for element in query_elements:
        #     if bloom_filter.query(element):
        #         if element in true_elements:
        #             true_positives += 1
        #         else:
        #             false_positives += 1
        #     else:
        #         true_negatives += 1

    
    print(f"true elements count: {len(true_elements)} true pos:{true_positives}, true_negatives: {true_negatives}, true negatives count: {len(false_elements)} false negatives: {false_negatives}  false pos: {false_positives}")

    observed_false_positive_prob = false_positives / (num_trials * expected_elements)
    observed_true_negative_rate = true_negatives / (num_trials * expected_elements)
    return observed_false_positive_prob, observed_true_negative_rate


# Simulation parameters
expected_elements = 100
false_positive_prob = 0.01  # 1% false positive probability
num_trials = 1

observed_false_positive_prob, observed_true_negative_rate = simulate_bloom_filter(
    expected_elements, false_positive_prob, num_trials
)

# print(f"Expected False Positive Probability: {false_positive_prob}")
# print(f"Observed False Positive Probability: {observed_false_positive_prob}")
# print(f"Observed True Negative Rate: {observed_true_negative_rate}")