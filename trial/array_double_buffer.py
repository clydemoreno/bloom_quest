import threading
import time
import random
import signal
import resource

class ThreadSafeArray:
    def __init__(self):
        self.array = []
        self.new_array = []
        self.lock = threading.Lock()

    def read(self, index):
        with self.lock:
            if len(self.array) > 0 and index < len(self.array):
                return self.array[index]
            else:
                return None

    def write(self, new_array):
        with self.lock:
            self.new_array = new_array

            # Swap the arrays to update the data
            self.array, self.new_array = self.new_array, self.array



def reader(thread_safe_array, index):
    while not exit_signal.is_set():
        value = thread_safe_array.read(index)
        duration = random.randint(1, 5)
        time.sleep(duration)
        print(f"Read value at index {index}: {value}. Memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}  KB  \r")

def writer(thread_safe_array, new_array):
    while not exit_signal.is_set():
        thread_safe_array.write(new_array)
        duration = random.randint(1, 5)
        time.sleep(duration)
        print(f"Array replaced with a new array. Memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss} KB \r")

def keyboard_interrupt_handler(signal, frame):
    print("Keyboard interrupt received. Stopping...")
    exit_signal.set()

if __name__ == "__main__":

    exit_signal = threading.Event()
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    ts_array = ThreadSafeArray()

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

