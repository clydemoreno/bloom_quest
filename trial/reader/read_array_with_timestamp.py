import os
import numpy as np
import re
from pathlib import Path

def load_array(path, file_name_pattern):
    # Get a list of files that match the file name pattern in the directory
    matching_files = list(path.glob(f"{file_name_pattern}_*.npy"))

    if not matching_files:
        raise FileNotFoundError(f"No matching files found for {file_name_pattern} in {path}")

    # Sort matching_files based on the timestamp in the filename (in reverse order)
    matching_files.sort(reverse=True, key=lambda file: int(re.search(r'\d{14}', str(file)).group()))


    # Get the latest file
    latest_file = matching_files[0]

    # Load the array from the latest file
    loaded_array = np.load(latest_file)

    return loaded_array

# # Example usage:
# # Specify the directory and file name pattern
# directory_path = Path("/path/to/your/directory")
# file_name_pattern = "test_data"

# # Load the latest array
# latest_loaded_array = load_array(directory_path, file_name_pattern)

# # Now you can use latest_loaded_array as needed
