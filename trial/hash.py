import time
def murmur_hash(input_string, seed):
    m = 0x5bd1e995
    r = 24
    length = len(input_string)
    
    h = seed ^ length
    
    for i in range(0, length, 4):
        k = ord(input_string[i]) | (ord(input_string[i + 1]) << 8) | (ord(input_string[i + 2]) << 16) | (ord(input_string[i + 3]) << 24)
        k = (k * m) & 0xffffffff
        k ^= (k >> r)
        k = (k * m) & 0xffffffff
        
        h = (h * m) & 0xffffffff
        h ^= k
    
    h ^= h >> 13
    h = (h * m) & 0xffffffff
    h ^= h >> 15
    
    return h

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
