import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
num_trials = 10000
hit_probabilities = np.arange(0.1, 1.0, 0.1)  # Cache hit probabilities from 0.1 to 0.9
latency_ratios = np.arange(0.2, 1.1, 0.1)  # Latency ratios from 0.2 to 1.0
average_latencies = np.zeros((len(hit_probabilities), len(latency_ratios)))

# Simulate cache access for varying hit probabilities and latency ratios
for i, hit_probability in enumerate(hit_probabilities):
    for j, latency_ratio in enumerate(latency_ratios):
        total_latency = 0

        for _ in range(num_trials):
            if random.random() < hit_probability:
                latency = random.randint(10, 20)  # Cache hit latency range
            else:
                # Adjust latency based on the ratio
                latency = random.randint(60, 90) * latency_ratio

            total_latency += latency

        average_latency = total_latency / num_trials
        average_latencies[i, j] = average_latency

# Create 3D surface plot
X, Y = np.meshgrid(hit_probabilities, latency_ratios)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, average_latencies.T, cmap='viridis')
ax.set_xlabel('Cache Hit Probability')
ax.set_ylabel('Latency Ratio (Miss/Hit)')
ax.set_zlabel('Average Latency (ms)')
ax.set_title('Cache Hit Probability vs. Latency Ratio vs. Average Latency')
plt.show()
