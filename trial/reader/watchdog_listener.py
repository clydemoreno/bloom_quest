import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil
import threading
from pathlib import Path
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return  # Ignore directory creation events
        print(f"File created: {event.src_path}")


class MemoryMonitor(threading.Thread):
    def __init__(self, interval=3):
        super().__init__()
        self.interval = interval
        self.stop_event = threading.Event()

    def run(self):
        process = psutil.Process()
        start_memory_usage = process.memory_info().rss / 1024  # in KB

        while not self.stop_event.is_set():
            memory = psutil.virtual_memory()
            print(f"Memory Usage: Total={memory.total}B, Available={memory.available}B, Used={memory.used}B, Free={memory.free}B")
            end_memory_usage = process.memory_info().rss / 1024  # in KB
            memory_usage_diff = end_memory_usage - start_memory_usage
            print(f"Memory used by the script: {memory_usage_diff} KB")
            
            time.sleep(self.interval)

    def stop(self):
        self.stop_event.set()


if __name__ == "__main__":
    # Define the directory to monitor
    parent_dir = Path(__file__).resolve().parent
    folder_to_watch = str(parent_dir)
    memory_monitor = MemoryMonitor()


    # Create an observer and attach the event handler
    observer = Observer()
    observer.schedule(MyHandler(), path=folder_to_watch, recursive=False)


    try:
        # Start monitoring
        observer.start()
        print(f"Watching for file creation events in {folder_to_watch}. Press Ctrl+C to stop.")
        memory_monitor.start()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # Stop and join the observer to terminate the monitoring gracefully
    observer.stop()
    observer.join()
