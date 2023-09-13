import threading
import time

class PeriodicTask:
    _instance = None

    def __new__(cls, callback, interval_seconds):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.callback = callback
            cls._instance.interval_seconds = interval_seconds
            cls._instance._stop_event = threading.Event()
            cls._instance.thread = threading.Thread(target=cls._instance._run)
            cls._instance.thread.daemon = True
            cls._instance.thread.start()
        return cls._instance

    def _run(self):
        while not self._stop_event.is_set():
            self.callback("Periodic task is running.")
            time.sleep(self.interval_seconds)

    def stop(self):
        self._stop_event.set()

# Example callback function
def example_callback(message):
    print(message)

if __name__ == "__main__":
    # Usage
    periodic_task = PeriodicTask(callback=example_callback, interval_seconds=5)
    try:
        # Keep the main thread running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        periodic_task.stop()
