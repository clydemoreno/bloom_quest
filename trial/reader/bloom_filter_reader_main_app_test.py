import asyncio
import sys
from pathlib import Path
import signal

import psutil

# Add the current directory to the sys.path
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))


from bloom_filter_reader import BloomFilterReader


from handler_event import HandlerEvent









# Define an observer class for testing
class TestObserver:
    async def update(self, message):
        memory_info = psutil.Process().memory_info()
        print(f"Received notification: {message}. Memory Usage: {memory_info.rss} bytes", end="\r")


# Main testing function




# ... (other imports and code)

async def main():
    # Create a BloomFilterReader with a time interval of 5 seconds
    reader = BloomFilterReader(time_interval_seconds=5)

    # Example usage:
    async def my_callback():
        
        # print("Callback executed", end="\r")  # Keep printout on the same line
        await reader.notify("Event callback executed")

    # Attach some test observers
    observer1 = TestObserver()
    observer2 = TestObserver()
    await reader.attach(observer1)
    await reader.attach(observer2)

    # Simulate an event by calling await asyncio.sleep(1)

    event_handler = HandlerEvent(my_callback, time_interval_seconds=5)

    # Register a signal handler for SIGTERM
    def sigterm_handler(signum, frame):
        print("Received SIGTERM. Stopping...", end="\n")  # Move to a new line
        event_handler.stop()
        asyncio.get_event_loop().stop()

    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        event_handler.start()
        await asyncio.Event().wait()
    except Exception as e:
        print(f"Caught exception: {e}. Stopping...", end="\n")  # Move to a new line
        event_handler.stop()
        asyncio.get_event_loop().stop()
    finally:
        asyncio.get_event_loop().close()

if __name__ == "__main__":
    asyncio.run(main())








# async def main():
#     # Create a BloomFilterReader with a time interval of 5 seconds
#     reader = BloomFilterReader(time_interval_seconds=5)

#     # Example usage:
#     async def my_callback():
#         print("Callback executed")
#         await reader.notify("Event callback executed")

#     # Attach some test observers
#     observer1 = TestObserver()
#     observer2 = TestObserver()
#     await reader.attach(observer1)
#     await reader.attach(observer2)

#     # Simulate an event triggering the notification
#     await asyncio.sleep(1)  # Wait for more than the time interval
#     await reader.notify("Event 1")

#     event_handler = HandlerEvent(my_callback, time_interval_seconds=5)

#     try:
#         event_handler.start()
#         await asyncio.Event().wait()
#     except KeyboardInterrupt:
#         # Handle Ctrl-C gracefully
#         pass
#     finally:
#         # Stop the handler
#         event_handler.stop()
