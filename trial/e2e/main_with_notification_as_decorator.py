import sys
import aiomysql
import asyncio
import os
import grpc
from pathlib import Path

sys_path = Path(__file__).resolve().parent.parent
sys_path_str = str(sys_path)
if sys_path_str not in sys.path:
    sys.path.append(sys_path_str)

from writer.mysql_data_writer import MySqlDataWriter
from writer.data_writer_interface import IDataWriter
from utility.load_config import load_config
from web import notification_pb2_grpc as my_grpc_pb2_grpc
from web import notification_pb2 as my_grpc_pb2

def grpc_notification(func):
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)  # Call the main function first
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
        
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = my_grpc_pb2_grpc.NotificationServiceStub(channel)
            request = my_grpc_pb2.NotificationRequest(message="Hello from Client!")
            response = stub.TriggerNotification(request)
            print("Response from server:", response.result)

        return result

    return wrapper

@grpc_notification
async def main():
    # Load configuration data
    config_data = load_config()

    # Create a MySQL data writer instance
    repository = MySqlDataWriter(config_data)

    # Call the build_array function
    array_length = await repository.build_array()
    print(f"Array built with {array_length} elements.")

if __name__ == '__main__':
    asyncio.run(main())
