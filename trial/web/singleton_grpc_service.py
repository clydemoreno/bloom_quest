import grpc
from concurrent import futures
import notification_pb2 as my_grpc_pb2
import notification_pb2_grpc as my_grpc_pb2_grpc

class SingletonGRPCService:
    def __init__(self, notification_callback):
        self._notification_callback = notification_callback
        self._init_service()

    def _init_service(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        my_grpc_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(self._notification_callback), self.server)
        self.server.add_insecure_port('[::]:50052')

    def start_service(self):
        self.server.start()

    def wait_for_termination(self):
        self.server.wait_for_termination()

class NotificationService(my_grpc_pb2_grpc.NotificationServiceServicer):
    def __init__(self, notification_callback):
        self._notification_callback = notification_callback

    def TriggerNotification(self, request, context):
        message = request.message
        # Call the callback function to handle the notification
        result = self._notification_callback(message)
        return my_grpc_pb2.NotificationResponse(result=result)
