import time
import matplotlib.pyplot as plt
import numpy as np
import sys
from pathlib import Path

# Get the parent directory of the current script (where the hash function module is located)
module_dir = Path(__file__).resolve().parent

# Add the parent directory to sys.path
sys.path.append(str(module_dir))

# Now you can import the hash function module directly
from super_fast_hash_func import SuperFastHash  # Updated import
from murmur_hash_func import MurmurHash  # Updated import

from sha256_hash_func import SHA256Hash  # Updated import


# Define the input string and the number of iterations
input_string = "Hello, World!"
num_iterations = 10000

# Initialize instances of the hash functions
hash_functions = [
    MurmurHash(),
    SuperFastHash(),
    SHA256Hash()
]

# Dictionary to store execution times
execution_times = {}

for func in hash_functions:
    execution_times[func.__class__.__name__] = []

# Measure execution times for each hash function
for func in hash_functions:
    for _ in range(num_iterations):
        start_time = time.perf_counter()
        func.hash(input_string)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        execution_times[func.__class__.__name__].append(execution_time)

# Calculate medians
medians = {}
for func_name, times in execution_times.items():
    medians[func_name] = np.median(times)

# Calculate the baseline (median of all medians)
baseline = np.median(list(medians.values()))

# Plot the execution times relative to the baseline
function_names = list(medians.keys())
relative_times = [median / baseline for median in medians.values()]

plt.figure(figsize=(10, 6))
plt.barh(function_names, relative_times, color='skyblue')
plt.xlabel('Relative Execution Time (compared to baseline)')
plt.title('Hash Function Execution Times Relative to Baseline')
plt.gca().invert_yaxis()
plt.axvline(x=1.0, color='red', linestyle='--', label='Baseline')
plt.legend()
plt.show()
