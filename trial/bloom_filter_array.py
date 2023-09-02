import threading
import numpy as np

class BloomFilterArray:
    def __init__(self, size, initialize_with_ones=False):
        self.size = size
        if initialize_with_ones:
            self.array = np.ones(size, dtype=np.int32)
        else:
            self.array = np.zeros(size, dtype=np.int32)
        self.lock = threading.Lock()

    def read(self, index):
        with self.lock:
            if 0 <= index < self.size:
                return self.array[index]
            else:
                return None

    def write(self, new_array):
        with self.lock:
            if len(new_array) == self.size:
                self.array = np.array(new_array, dtype=np.int32)
            else:
                print(f"New array must have size {self.size}")
