import unittest
import numpy as np
from pathlib import Path
import os
import tempfile
import time

# Import the load_array function from your code
from read_array_with_timestamp import load_array

class TestLoadArray(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = self.temp_dir.name

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_load_latest_array(self):
        # Create test files with timestamps in filenames
        file_name_pattern = "data"
        for i in range(1, 6):
            timestamp = time.strftime("%Y%m%d%H%M%S")
            file_name = f"{file_name_pattern}_{timestamp}.npy"
            file_path = os.path.join(self.temp_dir_path, file_name)
            np.save(file_path, np.array([i]))

        # Load the latest array
        latest_loaded_array = load_array(self.temp_dir_path, file_name_pattern)

        # Assert that the loaded array is correct
        self.assertTrue(np.array_equal(latest_loaded_array, np.array([5])))

if __name__ == '__main__':
    unittest.main()
