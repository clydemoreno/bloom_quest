import asyncio

class HandlerEvent:
    def __init__(self, callback, time_interval_seconds=3600):
        self.callback = callback
        self.time_interval_seconds = time_interval_seconds
        self.running = False
        self.lock = None  # No need to create the lock here
        self.loop = None  # No need to create the loop here

    async def run_periodically(self):
        while self.running:
            await asyncio.sleep(self.time_interval_seconds)
            if self.running:
                await self.callback()

    def start(self):
        if not self.running:
            self.running = True
            self.lock = asyncio.Lock()
            self.loop = asyncio.new_event_loop()  # Create a new event loop
            asyncio.set_event_loop(self.loop)  # Set the new event loop as current
            self.loop.create_task(self.run_periodically())

    def stop(self):
        self.running = False
