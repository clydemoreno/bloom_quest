import random
import time
import matplotlib.pyplot as plt

# Constants
cache_hit_latency_range = (10, 20)  # Latency range for cache hit in ms
cache_miss_latency_range = (60, 90)  # Latency range for cache miss in ms
num_trials = 10

# Create lists to store hit probabilities and corresponding average latencies
hit_probabilities = []
average_latencies = []

# Simulate cache access for varying hit probabilities
for hit_probability in range(10, 91, 10):  # Vary from 10% to 90%
    hit_probability = hit_probability / 100.0  # Convert to decimal
    total_latency = 0

    for _ in range(num_trials):
        if random.random() < hit_probability:
            latency = random.randint(*cache_hit_latency_range)
        else:
            latency = random.randint(*cache_miss_latency_range)
        total_latency += latency

    average_latency = total_latency / num_trials
    hit_probabilities.append(hit_probability)
    average_latencies.append(average_latency)

# Plot hit probabilities vs. average latencies
plt.plot(hit_probabilities, average_latencies, marker='o')
plt.title('Cache Hit Probability vs. Average Latency')
plt.xlabel('Cache Hit Probability')
plt.ylabel('Average Latency (ms)')
plt.grid(True)
plt.show()
