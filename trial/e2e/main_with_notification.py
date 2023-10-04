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


async def main():
    # Load configuration data
    config_data = load_config()

    # Create a MySQL data writer instance
    repository = MySqlDataWriter(config_data)

    try:
        # Call the build_array function
        array_length = await repository.build_array()
        print(f"Array built with {array_length} elements.")

        # Notify the gRPC service
        trigger_notification()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def trigger_notification():
    # Create a gRPC channel to connect to the server
    with grpc.insecure_channel('localhost:50052') as channel:
        # Create a gRPC stub
        stub = my_grpc_pb2_grpc.NotificationServiceStub(channel)

        # Define the request message
        request = my_grpc_pb2.NotificationRequest(message="Hello from Client!")

        # Call the gRPC service to trigger the notification
        response = stub.TriggerNotification(request)

        # Print the response from the server
        print("Response from server:", response.result)

if __name__ == '__main__':
    asyncio.run(main())
