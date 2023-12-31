import time
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import threading

class EventHandler(FileSystemEventHandler):
    def __init__(self, folder_path: str, callback: any):
        self.callback = callback
        self.file_observer = Observer()
        self.file_observer.schedule(self, path=folder_path, recursive=False)
        self.file_observer.start()

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"File created: {event.src_path}")
        self.callback(event.src_path)

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
    parent_dir = Path(__file__).resolve().parent
    folder_to_watch = str(parent_dir)

    event_handler = EventHandler(folder_to_watch, lambda x: None)  # Dummy callback
    memory_monitor = MemoryMonitor()

    print(f"Listening for file creation events in {folder_to_watch}. Press Ctrl+C to stop.")

    try:
        memory_monitor.start()
        while True:
            pass
    except KeyboardInterrupt:
        event_handler.file_observer.stop()
        event_handler.file_observer.join()
        memory_monitor.stop()
        memory_monitor.join()
