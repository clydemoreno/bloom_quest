import hashlib
import concurrent.futures
import time
from murmur_hash import murmur_hash 




# Hash function using hashlib.sha256
def sha256_hash(value, seed):
    start_time = time.time()
    hash_val = hashlib.sha256(value.encode() + bytes([seed])).hexdigest()
    int(hash_val, 16)  # Convert to integer (this is just for timing)
    end_time = time.time()
    return end_time - start_time

# Hash function using built-in hash
def builtin_hash(item, seed):
    start_time = time.time()
    hash(item + str(seed))  # Use the built-in hash function (this is just for timing)
    end_time = time.time()
    return end_time - start_time

# Hash function using MurmurHash
def murmur_hash_fn(value, seed):
    start_time = time.time()
    murmur_hash(str(value), seed, desired_length=16)


    end_time = time.time()
    return end_time - start_time

# Number of trials
num_trials = 1000  # Adjust the number of trials as needed

# Input data (e.g., strings)
input_data = ["apple", "banana", "cherry", "date", "elderberry"]

def time_hash_function(hash_function):
    total_time = 0.0
    for _ in range(num_trials):
        for item in input_data:
            for seed in range(10):  # Example: 10 seeds
                total_time += hash_function(item, seed)
    return total_time

# Measure execution time using concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    future_sha256 = executor.submit(time_hash_function, sha256_hash)
    future_builtin = executor.submit(time_hash_function, builtin_hash)
    future_murmur = executor.submit(time_hash_function, murmur_hash_fn)

# Get the results
sha256_time = future_sha256.result()
builtin_time = future_builtin.result()
murmur_time = future_murmur.result()

# Print the results
print(f"Execution time for hashlib-based hash (SHA-256): {sha256_time:.6f} seconds")
print(f"Execution time for built-in hash: {builtin_time:.6f} seconds")
print(f"Execution time for MurmurHash: {murmur_time:.6f} seconds")

# Compare the results
if sha256_time < builtin_time and sha256_time < murmur_time:
    print("SHA-256 is the winner.")
elif builtin_time < sha256_time and builtin_time < murmur_time:
    print("Built-in hash is the winner.")
else:
    print("MurmurHash is the winner.")



# Hash function using hashlib.sha256
def sha256_hash(value, seed):
    start_time = time.time()
    hash_val = hashlib.sha256(value.encode() + bytes([seed])).hexdigest()
    int(hash_val, 16)  # Convert to integer (this is just for timing)
    end_time = time.time()
    return end_time - start_time

# Hash function using built-in hash
def builtin_hash(item, seed):
    start_time = time.time()
    hash(item + str(seed))  # Use the built-in hash function (this is just for timing)
    end_time = time.time()
    return end_time - start_time

# Number of trials
num_trials = 1000  # Adjust the number of trials as needed

# Input data (e.g., strings)
input_data = ["apple", "banana", "cherry", "date", "elderberry"]

def time_hash_function(hash_function):
    total_time = 0.0
    for _ in range(num_trials):
        for item in input_data:
            for seed in range(10):  # Example: 10 seeds
                total_time += hash_function(item, seed)
    return total_time

# Measure execution time using concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future_sha256 = executor.submit(time_hash_function, sha256_hash)
    future_builtin = executor.submit(time_hash_function, builtin_hash)

# Get the results
sha256_time = future_sha256.result()
builtin_time = future_builtin.result()

# Print the results
print(f"Execution time for hashlib-based hash: {sha256_time:.6f} seconds")
print(f"Execution time for built-in hash: {builtin_time:.6f} seconds")
