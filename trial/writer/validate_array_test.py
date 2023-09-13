import unittest
import numpy as np
from validate_array import validate_array

class TestValidateArray(unittest.TestCase):
    def test_no_intersection(self):
        # Define a sample 'ids' list for testing
        sample_ids = [{'ID': 1}, {'ID': 2}, {'ID': 3}]

        # Create a NumPy array of false elements
        false_elements = np.array(['100001', '100002', '100003'])

        # Define a set of true elements (IDs as strings)
        true_elements = {'1', '2', '3'}

        # Define a Bloom filter mock object (replace with your actual Bloom filter)
        class BloomFilterMock:
            def check(self, item):
                # Mock the check method
                return item in true_elements

        # Create an instance of the BloomFilterMock
        bf_mock = BloomFilterMock()

        # Call the validate_array function with the mock and set initial=True
        validate_array(sample_ids, bf_mock, initial=True)

        # Check that there is no intersection between false_elements and true_elements
        intersection = set(false_elements) & true_elements
        self.assertEqual(len(intersection), 0)

if __name__ == '__main__':
    unittest.main()
