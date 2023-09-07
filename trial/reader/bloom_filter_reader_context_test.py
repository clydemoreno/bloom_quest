import asyncio
import atexit
import signal
from pathlib import Path
import sys

# Add the current directory to the sys.path
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

from bloom_filter_reader_context import BloomFilterReaderContext
from concrete_observer import ConcreteObserver

async def my_callback():
    print("Callback executed")

if __name__ == "__main__":
    folder_to_watch = "/path/to/watch"  # Set the correct path
    observer = ConcreteObserver()
    
    # Create the BloomFilterReaderContext as a context manager
    with BloomFilterReaderContext(folder_to_watch, my_callback, observer) as reader_context:
        # Register a cleanup handler to stop the context manager
        atexit.register(lambda: reader_context.__aexit__(None, None, None))
        
        try:
            # Run the event loop indefinitely
            reader_context.loop.run_forever()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Stop the context manager
            reader_context.__aexit__(None, None, None)
