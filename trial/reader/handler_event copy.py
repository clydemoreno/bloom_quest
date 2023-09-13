import asyncio

class HandlerEvent:
    def __init__(self, callback, time_interval_seconds=3600):

        self.callback = callback
        self.time_interval_seconds = time_interval_seconds
        self.running = False
        self.lock = asyncio.Lock()
        self.loop = None


    async def run_periodically(self):
        while self.running:
            await asyncio.sleep(self.time_interval_seconds)  # Sleep for the specified interval
            async with self.lock:
                if self.running:  # Check if still running after the sleep
                    await self.callback()

    def start(self):
        if not self.running:
            self.running = True
            self.loop = asyncio.get_event_loop()  # Get the current event loop
            self.loop.create_task(self.run_periodically())  # Use the current event loop to create the task

    def stop(self):
        self.running = False

# Example usage:
# async def my_callback():
#     print("Callback executed")

# if __name__ == "__main__":
#     # Create an asyncio event loop
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
    
#     folder_to_watch = "/path/to/watch"  # Set the correct path
#     event_handler = HandlerEvent(my_callback, time_interval_seconds=5)
    
#     # Start the handler
#     event_handler.start()
    
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         # Handle Ctrl-C gracefully
#         pass
#     finally:
#         # Stop the handler and close the event loop
#         event_handler.stop()
#         loop.close()
