
import threading
import numpy as np

class BloomFilterArray:
    def __init__(self, size, initialize_with_ones=False):
        self.size = size
        if initialize_with_ones:
            self.array = np.ones(self.size, dtype=np.int32)
        else:
            self.array = np.zeros(self.size, dtype=np.int32)
        self.lock = threading.Lock()

    def read(self, index):
        with self.lock:
            if 0 <= index < self.size:
                return self.array[index]
            else:
                return None

    def write(self, new_array):
        with self.lock:
            if isinstance(new_array, np.ndarray) and new_array.size == self.size:
                self.array = new_array.astype(np.int32)
            elif isinstance(new_array, list) and len(new_array) == self.size:
                self.array = np.array(new_array, dtype=np.int32)
            else:
                raise ValueError(f"New array must have size {self.size} and be a NumPy array or a list of the correct size")

# Rest of your test cases...




# import threading
# import numpy as np

# class BloomFilterArray:
#     def __init__(self, size, initialize_with_ones=False):
#         self.size = size
#         if initialize_with_ones:
#             self.array = np.ones(self.size, dtype=np.int32)
#         else:
#             self.array = np.zeros(self.size, dtype=np.int32)
#         self.lock = threading.Lock()

#     def read(self, index):
#         with self.lock:
#             if 0 <= index < self.size:
#                 return self.array[index]
#             else:
#                 return None

#     def write(self, new_array):
#             with self.lock:
#                 if isinstance(new_array, np.ndarray):
#                     self.array = new_array.astype(np.int32)
#                 # elif isinstance(new_array, list) and len(new_array) == self.size:
#                 #     self.array = np.array(new_array, dtype=np.int32)
#                 else:
#                     print(f"New array must have size {self.size} and be a NumPy array or a list of the correct size")



if __name__ == "__main__":

        size = 5
        bf = BloomFilterArray(size)
        np_array = np.array([60, 70, 80, 90, 100], dtype=np.int32)
        bf.write(np_array)
        for i in range(size):
            print(bf.read(i), np_array[i])
