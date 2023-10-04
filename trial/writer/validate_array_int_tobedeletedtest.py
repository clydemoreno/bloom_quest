import numpy as np
from validate_array import validate_array
import asyncio
import sys
from pathlib import Path

# Append the parent directory to the sys.path if necessary
sys.path.append(str(Path(__file__).resolve().parent.parent / "db"))  # Adjust the path as needed
from order_repository import OrderRepository


# Append the parent directory to the sys.path if necessary
sys.path.append(str(Path(__file__).resolve().parent.parent))
from bloom_filter_sha256 import BloomFilter


def validate_with_bloom_filter():


    # db_params

    # # Define a sample 'ids' list for testing

    # # [{'ID': 1}, {'ID': 2}, {'ID': 3}]
    # order_repository = OrderRepository(db_params)

    # sample_ids =   order_repository.get_all_ids() 

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

    if len(intersection) == 0:
        print("Test passed: No intersection between false_elements and true_elements.")
    else:
        print("Test failed: There is an intersection between false_elements and true_elements.")



asyncio.run(validate_with_bloom_filter())