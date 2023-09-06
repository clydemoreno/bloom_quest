import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

class EventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
    def on_created(self, event):
        if event.is_directory:
            return
        print(f"File created: {event.src_path}")
        self.callback(event.src_path)

# if __name__ == "__main__":

#     folder_to_watch = Path(".")  # Set the folder path you want to monitor here
#     event_handler = EventHandler()
#     observer = Observer()
#     observer.schedule(event_handler, folder_to_watch, recursive=False)

#     print(f"Listening for file creation events in {folder_to_watch}. Press Ctrl+C to stop.")

#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
