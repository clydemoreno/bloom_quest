
from murmur_hash import murmur_hash
import time

input_string = "9874"
seeds = [1, 2, 3]

for seed in seeds:
    start_time = time.time()
    
    # Call the function you want to measure
    result = murmur_hash(input_string, seed)
    
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"Hash result for seed {seed}: {result}")
    print(f"Execution time for seed {seed}: {execution_time:.6f} seconds\n")
