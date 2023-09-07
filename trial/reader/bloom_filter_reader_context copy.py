import asyncio
import atexit
import signal
from pathlib import Path
import sys
# Add the current directory to the sys.path
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

from handler_event import HandlerEvent
from bloom_filter_reader import BloomFilterReader

class BloomFilterReaderContext:
    def __init__(self, folder_to_watch, callback, observer, time_interval_seconds=5):
        self.folder_to_watch = folder_to_watch
        self.callback = callback
        self.time_interval_seconds = time_interval_seconds
        self.reader = None
        self.loop = None
        self.observer = observer  # Pass the observer as an argument

    async def __aenter__(self):
        # Create an asyncio event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Create the BloomFilterReader and attach the provided observer
        self.reader = BloomFilterReader()
        self.reader.attach(self.observer)

        # Create and start the HandlerEvent with the provided callback
        event_handler = HandlerEvent(self.callback, self.time_interval_seconds)
        event_handler.start()

        # Register a cleanup handler to stop the HandlerEvent and detach the observer
        atexit.register(self.cleanup_handler)
        
        # Register a signal handler for custom signal 'SIGTERM' to stop the program
        signal.signal(signal.SIGTERM, self.signal_handler)

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        # Stop the HandlerEvent, detach the observer, and close the event loop
        self.cleanup_handler()

    def cleanup_handler(self):
        if self.reader:
            self.reader.detach(self.observer)  # Detach the observer
        if self.loop:
            self.loop.close()

    def signal_handler(self, signum, frame):
        # Custom signal handler to stop the program
        if self.reader:
            self.reader.detach(self.observer)  # Detach the observer
            self.reader = None