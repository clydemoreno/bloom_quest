import sys
import aiomysql
import asyncio
from datetime import datetime
import numpy as np
from pathlib import Path
import os
import re

sys.path.append(str(Path(__file__).resolve().parent))  # Adjust the path as needed

import bf_data_pb2 as pb  # Import your custom Protobuf module

# ... (other imports and path appends)

def save_protobuf_data_with_timestamp(custom_data, data_directory, file_name):
    """
    Save Protobuf data with a timestamp in the filename.

    Args:
        custom_data (protobuf message): The Protobuf message to save.
        data_directory (str): The directory path where the file will be saved.
        file_name (str): The base file name (without the timestamp).

    Returns:
        str: The full path to the saved file.
    """
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Append the timestamp to the original file name
    file_name_with_timestamp = f"{file_name}_{timestamp}.protobuf"

    # Specify the full path to the file
    file_path = Path(data_directory) / file_name_with_timestamp

    # Serialize the Protobuf message
    serialized_data = custom_data.SerializeToString()

    # Save the serialized data to the file
    with open(file_path, "wb") as file:
        file.write(serialized_data)

    return str(file_path)


# Modify the save_data_to_file function to use save_protobuf_data_with_timestamp
def save_data_to_file(array, hash_count: int, array_length: int, data_directory, file_name):
    """
    Save data to a file using Protobuf serialization with a timestamp in the filename.

    Args:
        array (list): The data to be saved.
        hash_count (int): The hash count.
        array_length (int): The array length.
        data_directory (str): The directory where the file will be saved.
        file_name (str): The base file name (without the timestamp).
    """
    # Create a Protobuf message to store the data
    custom_data = pb.CustomData()
    custom_data.array.extend(array)
    custom_data.hash_count = hash_count
    custom_data.array_length = array_length

    # Save the Protobuf data with a timestamp in the filename
    save_protobuf_data_with_timestamp(custom_data, data_directory, file_name)


# def save_data_to_file(array, hash_count: int, array_length: int,  data_directory, file_name):
#     """
#     Save data to a file using Protobuf serialization.
#     Args:
#         data_directory (str): The directory where the file will be saved.
#         file_name (str): The name of the file.
#     """
#     # Create a Protobuf message to store the data
#     custom_data = pb.CustomData()
#     custom_data.array.extend(array)
#     custom_data.hash_count = hash_count
#     custom_data.array_length = array_length

#     # Serialize the Protobuf message
#     serialized_data = custom_data.SerializeToString()

#     # Specify the full path to the file
#     file_path = Path(data_directory) / file_name

#     # Save the serialized data to the file
#     with open(file_path, "wb") as file:
#         file.write(serialized_data)


def load_data_from_file(data_directory, file_name_pattern):
    """
    Load and deserialize the latest Protobuf data file with a given file name pattern.
    
    Args:
        data_directory (str): The directory where the files are located.
        file_name_pattern (str): The base file name pattern (without the timestamp).

    Returns:
        Tuple: A tuple containing the loaded data (list), hash count (int), and array length (int).
    """
    # Construct the full file name pattern to search for
    full_pattern = f"{file_name_pattern}_*.protobuf"
    
    path = Path(data_directory)

    # Get a list of files that match the file name pattern in the directory
    matching_files = list(path.glob(full_pattern))

    if not matching_files:
        raise FileNotFoundError(f"No matching files found for {full_pattern} in {path}")

    # Sort matching_files based on the timestamp in the filename (in reverse order)
    matching_files.sort(reverse=True, key=lambda file: int(re.search(r'\d{14}', str(file)).group()))

    # Get the latest file
    latest_file = matching_files[0]

    custom_data = pb.CustomData()

    # Load the data from the latest file
    with open(latest_file, "rb") as file:
        custom_data.ParseFromString(file.read())

    return custom_data.array, custom_data.hash_count, custom_data.array_length


# def load_data_from_file(file_path):
#     """
#     Load and deserialize data from a Protobuf file.
#     Args:
#         file_path (str): The path to the Protobuf file.
#     Returns:
#         Tuple: A tuple containing the loaded data (list), hash count (int), and array length (int).
#     """
#     custom_data = pb.CustomData()

#     # Load the data from the file
#     with open(file_path, "rb") as file:
#         custom_data.ParseFromString(file.read())

#     return custom_data.array, custom_data.hash_count, custom_data.array_length

# # Unit test to save, load, and verify data
# if __name__ == "__main__":
#     # Create an instance of MySqlDataWriter (provide necessary config_data)
#     data_writer = MySqlDataWriter(config_data)

#     # Build and save the data to a file
#     data_directory = "data"  # Specify your data directory
#     file_name = "custom_data.protobuf"  # Specify your file name
#     data_writer.build_array()
#     data_writer.save_data_to_file(data_directory, file_name)

#     # Load and verify the data from the file
#     loaded_data, loaded_hash_count, loaded_array_length = data_writer.load_data_from_file(Path(data_directory) / file_name)

#     # Verify the loaded data
#     assert loaded_data == data_writer.ids
#     assert loaded_hash_count == data_writer.bloom_filter.hash_count
#     assert loaded_array_length == len(data_writer.bloom_filter.bf_array.array)
