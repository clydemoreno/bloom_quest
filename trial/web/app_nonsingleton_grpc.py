import grpc
from concurrent import futures
import notification_pb2 as my_grpc_pb2
import notification_pb2_grpc as my_grpc_pb2_grpc
from flask import Flask, jsonify
import threading  # Import threading module

# Create a Flask app
app = Flask(__name__)

server = None


# gRPC service implementation
class NotificationService(my_grpc_pb2_grpc.NotificationServiceServicer):
    def TriggerNotification(self, request, context):
        message = request.message

        # Call br_subject.notify with the provided message
        print("Message:", message)

        return my_grpc_pb2.NotificationResponse(result="Notification triggered successfully")

def run_grpc_server():
    print("grpc started")
    global server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_grpc_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(), server)
    server.add_insecure_port('[::]:50052')  # Use a different port for gRPC
    server.start()
    server.wait_for_termination()
    print("grpc end")

# Define a Flask endpoint
@app.route('/api/hello')
def hello():
    return jsonify(message="Hello from Flask!")

if __name__ == '__main__':
    # Start the gRPC server in a separate thread
    grpc_thread = threading.Thread(target=run_grpc_server)
    grpc_thread.start()

    # Run the Flask app in the main thread
    app.run(debug=True, host='0.0.0.0', port=5000)
