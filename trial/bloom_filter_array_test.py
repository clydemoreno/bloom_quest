import threading
import time
import random
import signal
import resource
from bloom_filter_array import BloomFilterArray  # Update the import

# Rest of your code remains the same with the usage of BloomFilterArray


def reader(thread_safe_array, index):
    while not exit_signal.is_set():
        value = thread_safe_array.read(index)
        print(f"Read value at index {index}: {value}")
        duration = random.randint(1, 5)
        time.sleep(duration)
        print(f"Memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}  KB")

def writer(thread_safe_array, new_array):
    while not exit_signal.is_set():
        thread_safe_array.write(new_array)
        print("Array replaced with a new array")
        duration = random.randint(1, 5)
        time.sleep(duration)
        print(f"Memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss} KB")

def keyboard_interrupt_handler(signal, frame):
    print("Keyboard interrupt received. Stopping...")
    exit_signal.set()

if __name__ == "__main__":
    exit_signal = threading.Event()
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    ts_array = BloomFilterArray(size=5, initialize_with_ones=False)  # Adjust the size and initialization as needed

    SIM_SIZE = 1
    reader_threads = []
    writer_threads = []

    # Get initial memory usage
    initial_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    try:
        for _ in range(SIM_SIZE):
            for i in range(5):
                reader_thread = threading.Thread(target=reader, args=(ts_array, i))
                reader_threads.append(reader_thread)
                reader_thread.start()

                writer_thread = threading.Thread(target=writer, args=(ts_array, [10, 20, 30, 40, 50]))
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

    # Access the BloomFilterArray as a NumPy array
    numpy_array = ts_array.array
    print("NumPy array:", numpy_array)
