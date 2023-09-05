import numpy as np
from pathlib import Path
from datetime import datetime

def save_array_with_timestamp(data, path, file_name):
    """
    Save a NumPy array with a timestamp in the filename.

    Args:
        data (numpy.ndarray): The NumPy array to save.
        path (str): The directory path where the file will be saved.
        file_name (str): The base file name (without the timestamp).

    Returns:
        str: The full path to the saved file.
    """
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Append the timestamp to the original file name
    file_name_with_timestamp = f"{file_name}_{timestamp}.npy"

    # Create the full path by joining the directory and file name
    save_path = Path(path) / file_name_with_timestamp

    # Save the array to the specified path
    np.save(save_path, data)

    return str(save_path)
