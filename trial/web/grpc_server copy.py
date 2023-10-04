import grpc
from concurrent import futures
import notification_pb2 as my_grpc_pb2
import notification_pb2_grpc as my_grpc_pb2_grpc

class NotificationService(my_grpc_pb2_grpc.NotificationServiceServicer):
    def TriggerNotification(self, request, context):
        message = request.message

        # Call br_subject.notify with the provided message
        print("Message: ", message)

        return my_grpc_pb2.NotificationResponse(result="Notification triggered successfully")

def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_grpc_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(), server)
    server.add_insecure_port('[::]:50052')  # Use a different port for gRPC
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_grpc_server()
