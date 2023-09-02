import random
import multiprocessing
from bloom_filter_geek import BloomFilter


def worker_bloom_filter_check(bloom_filter, query_elements_chunk,false_elements, true_elements, result_queue):
    false_positives = 0
    true_negatives = 0
    true_positives = 0
    false_negatives = 0

    for element in true_elements:
        if  bloom_filter.check(element):
                true_positives += 1
        # else:
        #     true_negatives += 1


    # for element in query_elements_chunk:
    #     if not bloom_filter.check(element):
    #         if element in false_elements:
    #             true_negatives += 1
    #         else:
    #             false_negatives += 1
    #     else:
    #         if element in true_elements:
    #             false_positives += 1
    #         else:
    #             true_positives += 1

    result_queue.put((false_positives, true_negatives, true_positives, false_negatives))

def simulate_bloom_filter(expected_elements, false_positive_prob, num_trials):
    true_elements = [str(random.randint(1, 40000)) for _ in range(expected_elements)]
    false_elements = [str(random.randint(1, 40000)) for _ in range(expected_elements)]
    query_elements = true_elements + false_elements

    num_processes = multiprocessing.cpu_count()
    chunk_size = len(query_elements) // num_processes

    observed_false_positive_prob = 0
    observed_true_negative_prob = 0
    observed_true_positive_prob = 0
    observed_false_negative_prob = 0



    for _ in range(num_trials):
        bloom_filter = BloomFilter(expected_elements, false_positive_prob)

        for element in true_elements:
            bloom_filter.add(element)
        
        processes = []
        result_queue = multiprocessing.Queue()

        for i in range(num_processes):
            query_elements_chunk = query_elements[i * chunk_size: (i + 1) * chunk_size]
            p = multiprocessing.Process(target=worker_bloom_filter_check, args=(bloom_filter, query_elements_chunk, false_elements, true_elements,result_queue))
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

        observed_false_positive_prob += fp_sum / (num_trials * expected_elements)
        observed_true_negative_prob += tn_sum / (num_trials * expected_elements)
        observed_true_positive_prob += tp_sum / (num_trials * expected_elements)
        observed_false_negative_prob += fn_sum / (num_trials * expected_elements)

    return (
        observed_false_positive_prob / num_trials,
        observed_true_negative_prob / num_trials,
        observed_true_positive_prob / num_trials,
        observed_false_negative_prob / num_trials
    )

if __name__ == "__main__":
    expected_elements = 100
    false_positive_prob = 0.01
    num_trials = 10

    fp_prob, tn_prob, tp_prob, fn_prob = simulate_bloom_filter(expected_elements, false_positive_prob, num_trials)

    print("False Positive Probability:", fp_prob)
    print("True Negative Probability:", tn_prob)
    print("True Positive Probability:", tp_prob)
    print("False Negative Probability:", fn_prob)
