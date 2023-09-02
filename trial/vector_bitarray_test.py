import numpy as np
import time
import threading
import signal
import sys

size = 100000000

def numpy_bitwise_or(random_bits1, random_bits2):
    result_array = np.bitwise_or(random_bits1, random_bits2)

def list_bitwise_or(random_bits1, random_bits2):
    result_array = [a | b for a, b in zip(random_bits1, random_bits2)]

# Generate random bits (0 or 1)
random_bits1 = np.random.randint(2, size=size)
random_bits2 = np.random.randint(2, size=size)

def test_numpy():
    try:
        numpy_start_time = time.time()
        numpy_bitwise_or(random_bits1, random_bits2)
        numpy_end_time = time.time()
        return numpy_end_time - numpy_start_time
    except KeyboardInterrupt:
        print("NumPy test interrupted")

def test_list():
    try:
        list_start_time = time.time()
        list_bitwise_or(random_bits1, random_bits2)
        list_end_time = time.time()
        return list_end_time - list_start_time
    except KeyboardInterrupt:
        print("List test interrupted")

# Create threads for each test
numpy_result = 0
list_result = 0
numpy_thread = threading.Thread(target=lambda: setattr(numpy_thread, 'result', test_numpy()))
list_thread = threading.Thread(target=lambda: setattr(list_thread, 'result', test_list()))

# Register a signal handler for Ctrl+C
def signal_handler(sig, frame):
    print("\nCtrl+C received. Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Start both threads
numpy_thread.start()
list_thread.start()

# Wait for both threads to finish
numpy_thread.join()
list_thread.join()

# Retrieve results from threads
numpy_time = numpy_thread.result
list_time = list_thread.result

# Determine the faster approach and calculate speedup
if numpy_time < list_time:
    faster_approach = "NumPy"
    slower_time = list_time
    faster_time = numpy_time
    speedup_factor = slower_time / faster_time if faster_time != 0 else "N/A"
else:
    faster_approach = "List"
    slower_time = numpy_time
    faster_time = list_time
    speedup_factor = slower_time / faster_time if faster_time != 0 else "N/A"

print("Faster approach:", faster_approach)
print("Slower time:", slower_time)
print("Faster time:", faster_time)
print("Speedup factor (Slower time / Faster time):", speedup_factor)
