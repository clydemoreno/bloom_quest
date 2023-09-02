from bloom_filter_geek import BloomFilter
from bloom_filter_sha256 import BloomFilter as BloomFilterSha256
from bloom_filter_interface import IBloomFilter
from random import shuffle
import random
import multiprocessing


def worker_bloom_filter_check(expected_elements, false_positive_prob, query_elements_chunk,false_elements, true_elements, result_queue):

    bloom_filter = BloomFilter(expected_elements,false_positive_prob)

    false_positives = 0
    true_negatives = 0
    true_positives = 0
    false_negatives = 0



    # Insert true elements into the Bloom filter
    for element in true_elements:
        bloom_filter.add(element)

    for element in query_elements_chunk:
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

    result_queue.put((false_positives, true_negatives, true_positives, false_negatives))

def simulate_bloom_filter(expected_elements, false_positive_prob, num_trials):
    
    # Generate random data items
    true_elements = [str(random.randint(1, 10000)) for _ in range(expected_elements ) ]
    false_elements = [str(random.randint(20000, 30000)) for _ in range(expected_elements) ]
    query_elements = true_elements + false_elements

    processes = []
    result_queue = multiprocessing.Queue()

    num_processes = multiprocessing.cpu_count()

    chunk_size = len(query_elements) // num_processes

    for process in processes:
        process.join()

    for _ in range(num_trials):


        for i in range(num_processes):
            query_elements_chunk = query_elements[i * chunk_size: (i + 1) * chunk_size]
            p = multiprocessing.Process(target=worker_bloom_filter_check, args=(expected_elements, false_positive_prob,query_elements_chunk, false_elements, true_elements,result_queue))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()


            
        fp_sum, tn_sum, tp_sum, fn_sum = 0, 0, 0, 0
        for _ in range(num_processes):
            false_positives, true_negatives, true_positives, false_negatives = result_queue.get()
            fp_sum += false_positives
            tn_sum += true_negatives
            tp_sum += true_positives
            fn_sum += false_negatives

    observed_false_positive_prob = fp_sum / (num_trials * expected_elements)
    observed_true_negative_prob = tn_sum / (num_trials * expected_elements)
    observed_true_positive_prob = tp_sum / (num_trials * expected_elements)
    observed_false_negative_prob = fn_sum / (num_trials * expected_elements)

      

    return observed_false_positive_prob,observed_true_negative_prob, observed_true_positive_prob, observed_false_negative_prob

if __name__ == "__main__":

    # Simulation parameters
    expected_elements = 100
    false_positive_prob = 0.05  # 1% false positive probability
    num_trials = 50


    observed_false_positive_prob, observed_true_negative_prob,observed_true_positive_prob, observed_false_negative_prob = simulate_bloom_filter(expected_elements, false_positive_prob, num_trials)


    # print(f"Expected False Positive Probability: {false_positive_prob}")
    # print(f"Observed False Positive Probability: {observed_false_positive_prob}")
    # print(f"Observed True Negative Probability: {observed_true_negative_prob}")
    # print(f"Observed True Positive Probability: {observed_true_positive_prob}")
    # print(f"Observed False Negative Probability: {observed_false_negative_prob}")
