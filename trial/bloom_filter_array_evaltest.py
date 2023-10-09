import threading
import time
import random
import signal
import resource
from bloom_filter_array import BloomFilterArray  # Import BloomFilterArray from your separate file

def reader(bloom_filter_array, index):
    while not exit_signal.is_set():
        value = bloom_filter_array.read(index)
        duration = random.randint(1, 5)
        time.sleep(duration)
        print(f"Read value at index {index}: {value}. Memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss} KB  \r")

def writer(bloom_filter_array, new_array):
    while not exit_signal.is_set():
        bloom_filter_array.write(new_array)
        duration = random.randint(1, 5)
        time.sleep(duration)
        print(f"Array replaced with a new array. Memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss} KB \r")

def keyboard_interrupt_handler(signal, frame):
    print("Keyboard interrupt received. Stopping...")
    exit_signal.set()

if __name__ == "__main__":
    exit_signal = threading.Event()
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    bf_array = BloomFilterArray(size=5)

    SIM_SIZE = 1
    reader_threads = []
    writer_threads = []

    # Get initial memory usage
    initial_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    try:
        for _ in range(SIM_SIZE):
            for i in range(5):
                reader_thread = threading.Thread(target=reader, args=(bf_array, i))
                reader_threads.append(reader_thread)
                reader_thread.start()

                writer_thread = threading.Thread(target=writer, args=(bf_array, [10, 20, 30, 40, 50]))
                writer_threads.append(writer_thread)
                writer_thread.start()

        for reader_thread in reader_threads:
            reader_thread.join()

        for writer_thread in writer_threads:
            writer_thread.join()

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Stopping...")
        exit_signal.set()
    
    # Get final memory usage
    final_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    print(f"Initial memory usage: {initial_memory} KB")
    print(f"Final memory usage: {final_memory} KB")
