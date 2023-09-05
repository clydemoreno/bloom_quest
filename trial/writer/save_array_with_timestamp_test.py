import unittest
import os
from pathlib import Path
import numpy as np
from tempfile import TemporaryDirectory
from save_array_with_timestamp import save_array_with_timestamp

class TestFileSaver(unittest.TestCase):
    def test_save_array_with_timestamp(self):
        # Create a temporary directory for testing
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            # Create a NumPy array (example)
            my_array = np.array([1, 2, 3, 4, 5])

            # Specify the file name
            file_name = 'test_data'

            # Call the save function
            saved_file_path = save_array_with_timestamp(my_array, temp_dir_path, file_name)

            # Verify that the saved file exists
            self.assertTrue(os.path.exists(saved_file_path))

            # Extract the timestamp part from the saved file's name
            filename_without_extension = os.path.splitext(os.path.basename(saved_file_path))[0]
            timestamp_part = filename_without_extension[len(file_name) + 1:]  # Remove '<file_name>_'

            # Verify that the timestamp part is in the expected format (YYYYMMDDHHMMSS)
            self.assertRegex(timestamp_part, r'^\d{14}$')

            # Load the saved array
            loaded_array = np.load(saved_file_path)

            # Assert that the loaded array is identical to the original array
            np.testing.assert_array_equal(my_array, loaded_array)

if __name__ == '__main__':
    unittest.main()
