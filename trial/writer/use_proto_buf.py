import sys
import aiomysql
import asyncio
from datetime import datetime
import numpy as np
from pathlib import Path
import os
import bf_data_pb2 as mydata_pb2  # Import your custom Protobuf module

# ... (other imports and path appends)



def save_data_to_file(array, hash_count: int, array_length: int,  data_directory, file_name):
    """
    Save data to a file using Protobuf serialization.
    Args:
        data_directory (str): The directory where the file will be saved.
        file_name (str): The name of the file.
    """
    # Create a Protobuf message to store the data
    custom_data = mydata_pb2.CustomData()
    custom_data.array.extend(array)
    custom_data.hash_count = hash_count
    custom_data.array_length = array_length

    # Serialize the Protobuf message
    serialized_data = custom_data.SerializeToString()

    # Specify the full path to the file
    file_path = Path(data_directory) / file_name

    # Save the serialized data to the file
    with open(file_path, "wb") as file:
        file.write(serialized_data)

def load_data_from_file(file_path):
    """
    Load and deserialize data from a Protobuf file.
    Args:
        file_path (str): The path to the Protobuf file.
    Returns:
        Tuple: A tuple containing the loaded data (list), hash count (int), and array length (int).
    """
    custom_data = mydata_pb2.CustomData()

    # Load the data from the file
    with open(file_path, "rb") as file:
        custom_data.ParseFromString(file.read())

    return custom_data.array, custom_data.hash_count, custom_data.array_length

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
