import unittest
import random
from bit_or import bitwise_or, generate_random_bit_array

class TestBitwiseOr(unittest.TestCase):
    def test_bitwise_or_same_length(self):
        bit_array1 = [1, 0, 1, 0, 1]
        bit_array2 = [0, 1, 1, 0, 0]
        expected_result = [1, 1, 1, 0, 1]
        result = bitwise_or(bit_array1, bit_array2)
        self.assertEqual(result, expected_result)

    def test_bitwise_or_same_length_not_equal(self):
        bit_array1 = [1, 0, 1, 0, 1]
        bit_array2 = [0, 1, 1, 0, 0]
        expected_result = [0, 1, 1, 0, 1]
        result = bitwise_or(bit_array1, bit_array2)
        self.assertNotEqual(result, expected_result)


    def test_bitwise_or_different_length(self):
        bit_array1 = [1, 0, 1, 0, 1]
        bit_array2 = [0, 1, 1]
        expected_result = [1, 1, 1]
        result = bitwise_or(bit_array1, bit_array2)
        self.assertEqual(result, expected_result)

    def test_bitwise_or_random(self):
        # random.seed(42)  # Seed for reproducibility
        size = 10
        bit_array1 = generate_random_bit_array(size)
        bit_array2 = generate_random_bit_array(size)
        result = bitwise_or(bit_array1, bit_array2)
        if bit_array1[0] == 0 and bit_array2[0] == 0:
            self.assertEqual(result[0] , 0)
        if bit_array1[0] == 1 or bit_array2[0] == 1:
            self.assertEqual(result[0] , 1)
        
        if bit_array1[0] == 1 and bit_array2[0] == 1:
            self.assertEqual(result[0] , 1)

if __name__ == '__main__':
    unittest.main()
