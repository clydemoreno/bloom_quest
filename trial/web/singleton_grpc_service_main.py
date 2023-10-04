import singleton_grpc_service as grpc_service

# Define a custom callback function to handle notifications
def custom_notification_callback(message):
    # Customize the notification handling logic here
    print("Custom Notification: ", message)
    return "Custom Notification handled successfully"

def run_grpc_server(notification_callback):
    grpc_service_instance = grpc_service.SingletonGRPCService(notification_callback)
    grpc_service_instance.start_service()
    grpc_service_instance.wait_for_termination()

if __name__ == '__main__':
    run_grpc_server(custom_notification_callback)
