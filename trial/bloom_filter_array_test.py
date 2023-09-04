import unittest
from threading import Thread
from time import sleep
from random import randint
from bloom_filter_array import BloomFilterArray
import numpy as np

class TestBloomFilterArray(unittest.TestCase):
    def test_initialization(self):
        # Test initialization with zeros
        size = 10
        bf = BloomFilterArray(size)
        self.assertEqual(bf.size, size)
        self.assertTrue((bf.array == 0).all())

        # Test initialization with ones
        size = 5
        bf = BloomFilterArray(size, initialize_with_ones=True)
        self.assertEqual(bf.size, size)
        self.assertTrue((bf.array == 1).all())

    def test_read_and_write(self):
        size = 5
        bf = BloomFilterArray(size)

        # Test read before write
        for i in range(size):
            self.assertEqual(bf.read(i),0)

        # Test write and read
        new_array = [10, 20, 30, 40, 50]
        bf.write(new_array)
        for i in range(size):
            self.assertEqual(bf.read(i), new_array[i])

    def test_write_casting(self):
        size = 5
        bf = BloomFilterArray(size)

        # Test writing regular list
        new_array = [10, 20, 30, 40, 50]
        bf.write(new_array)
        self.assertTrue(isinstance(bf.array, np.ndarray))

        # Test writing NumPy array
        np_array = np.array([60, 70, 80, 90, 100], dtype=np.int32)
        bf.write(np_array)
        self.assertTrue(isinstance(bf.array, np.ndarray))
        self.assertTrue(np.array_equal(bf.array, np_array))            

if __name__ == '__main__':
    unittest.main()
