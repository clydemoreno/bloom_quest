import sys
from pathlib import Path

# Get the parent directory of the current script (test_handler_event.py)
current_script_dir = Path(__file__).resolve().parent

# Append the parent directory to sys.path to make the module importable
# module_parent_dir = current_script_dir.parent
# sys.path.append(str(module_parent_dir))

sys.path.append(str(current_script_dir))

import asyncio
from handler_event import HandlerEvent

# Example usage:
async def my_callback():
    print("Callback executed")

if __name__ == "__main__":
    
    event_handler = HandlerEvent(my_callback, time_interval_seconds=5)
    # Create an asyncio event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Start the handler
    event_handler.start()
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        # Handle Ctrl-C gracefully
        pass
    finally:
        # Stop the handler and close the event loop
        event_handler.stop()
        loop.close()
