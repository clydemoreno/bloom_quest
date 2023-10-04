import grpc
import notification_pb2_grpc as my_grpc_pb2_grpc
import notification_pb2 as  my_grpc_pb2

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
    trigger_notification()


