import asyncio
import sys
from pathlib import Path
import signal
import psutil
import time  # Import the time module for measuring memory usage delta

# Add the current directory to sys.path
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

from bloom_filter_reader import BloomFilterReader
from handler_event import HandlerEvent

# Define an observer class for testing
class TestObserver:
    def __init__(self):
        self.start_memory = None  # Store the initial memory usage
        self.max_memory_delta = 0  # Store the maximum memory delta observed

    async def update(self, message):
        memory_info = psutil.Process().memory_info()
        if self.start_memory is None:
            self.start_memory = memory_info.rss
        else:
            memory_delta = memory_info.rss - self.start_memory
            self.max_memory_delta = max(self.max_memory_delta, memory_delta)

        print(f"Received notification: {message}. Memory Usage: {memory_info.rss} bytes (Max Delta: {self.max_memory_delta} bytes)", end="\r")

# Main testing function
async def main():
    # Create a BloomFilterReader with a time interval of 5 seconds
    reader = BloomFilterReader(time_interval_seconds=5)

    # Attach some test observers
    observer1 = TestObserver()
    observer2 = TestObserver()
    await reader.attach(observer1)
    await reader.attach(observer2)


    # Example usage:
    async def my_callback():
        await reader.notify("Event callback executed")

    event_handler = HandlerEvent(my_callback, time_interval_seconds=5)

    # Register a signal handler for SIGTERM
    def sigterm_handler(signum, frame):
        print("Received SIGTERM. Stopping...", end="\n")
        event_handler.stop()
        asyncio.get_event_loop().stop()

    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        event_handler.start()
        await asyncio.Event().wait()
    except Exception as e:
        print(f"Caught exception: {e}. Stopping...", end="\n")
        event_handler.stop()
        asyncio.get_event_loop().stop()
    finally:
        asyncio.get_event_loop().close()

if __name__ == "__main__":
    asyncio.run(main())
