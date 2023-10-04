import unittest
import numpy as np
from bloom_filter_array import BloomFilterArray

class TestBloomFilterArray(unittest.TestCase):
    def test_initialization_with_zeros(self):
        size = 10
        bf = BloomFilterArray(size)
        self.assertEqual(bf.size, size)
        self.assertTrue((bf.array == 0).all())

    def test_initialization_with_ones(self):
        size = 5
        bf = BloomFilterArray(size, initialize_with_ones=True)
        self.assertEqual(bf.size, size)
        self.assertTrue((bf.array == 1).all())

    def test_read_valid_index(self):
        size = 5
        bf = BloomFilterArray(size)
        for i in range(size):
            self.assertEqual(bf.read(i), 0)

    def test_read_invalid_index(self):
        size = 5
        bf = BloomFilterArray(size)
        self.assertIsNone(bf.read(-1))
        self.assertIsNone(bf.read(size))
        self.assertIsNone(bf.read(size + 1))

    def test_write_list(self):
        # size = 5
        # bf = BloomFilterArray(size)
        # new_array = [10, 20, 30, 40, 50]
        # bf.write(new_array)
        # for i in range(size):
        #     self.assertEqual(bf.read(i), new_array[i])

        size = 5
        bf = BloomFilterArray(size)
        np_array = np.array([60, 70, 80, 90, 100], dtype=np.int32)
        bf.write(np_array)
        for i in range(size):
            print(bf.read(i), np_array[i])
            assert (bf.read(i) == np_array[i])
            self.assertEqual(bf.read(i), np_array[i])


    def test_write_numpy_array(self):
        size = 5
        bf = BloomFilterArray(size)
        np_array = np.array([60, 70, 80, 90, 100], dtype=np.int32)
        bf.write(np_array)
        self.assertTrue(isinstance(bf.array, np.ndarray))
        self.assertTrue(np.array_equal(bf.array, np_array))

    def test_write_invalid_input(self):
        size = 5
        bf = BloomFilterArray(size)
        invalid_array = [1, 2, 3]  # Invalid size
        with self.assertRaises(ValueError):
            bf.write(invalid_array)

if __name__ == '__main__':
    unittest.main()
