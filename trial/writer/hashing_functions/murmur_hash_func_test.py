import unittest
import random
import string

from pathlib import Path

import sys

# Get the parent directory of the current script (where the hash function module is located)
module_dir = Path(__file__).resolve().parent

# Add the parent directory to sys.path
sys.path.append(str(module_dir))

# Now you can import the hash function module directly
from murmur_hash_func import MurmurHash

class TestHashFunctions(unittest.TestCase):

    def setUp(self):
        # Initialize an instance of the hash function
        self.murmur_hasher = MurmurHash()

    def test_MurmurHash(self):
        # Generate and test 10 random input strings
        for _ in range(10):
            input_str = self.generate_random_string()
            actual_hash = self.murmur_hasher.hash(input_str)
            
            # Print input and hash for debugging
            print(f"Input: '{input_str}', Hash: {actual_hash}")
            
            # Assert that the hash is not None (just to ensure it's generated)
            self.assertIsNotNone(actual_hash)

    def generate_random_string(self, length=10):
        # Generate a random string of specified length
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

if __name__ == "__main__":
    unittest.main()
