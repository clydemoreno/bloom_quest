import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add the current directory to sys.path
current_directory = Path(__file__).resolve().parent
sys.path.append(str(current_directory))

from bf_data_pb2 import CustomData 

from use_proto_buf import save_data_to_file, load_data_from_file

class TestSaveLoadDataToFile(unittest.TestCase):
    def test_save_and_load_data(self):
        # Generate sample data
        sample_array = [1, 2, 3, 4, 5]
        sample_hash_count = 42
        sample_array_length = len(sample_array)

        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Convert the temporary directory path to a Path object
            temp_dir_path = Path(temp_dir)

            # Specify the file name
            file_name = "custom_data.protobuf"

            # Save the sample data to a file
            save_data_to_file(
                sample_array, sample_hash_count, sample_array_length, temp_dir_path, file_name
            )

            # Load the data from the file
            loaded_array, loaded_hash_count, loaded_array_length = load_data_from_file(
                temp_dir_path / file_name
            )

            # Verify the loaded data
            self.assertEqual(loaded_array, sample_array)
            self.assertEqual(loaded_hash_count, sample_hash_count)
            self.assertEqual(loaded_array_length, sample_array_length)

if __name__ == "__main__":
    unittest.main()
