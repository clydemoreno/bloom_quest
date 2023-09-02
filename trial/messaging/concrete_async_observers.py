from IAsyncObserver import IAsyncObserver
import asyncio
import random

class AsyncConcreteObserverA(IAsyncObserver):
    async def update(self, message):
        sleep_time = random.uniform(0.5, 2.0)  # Random sleep time between 0.5 and 2.0 seconds
        await asyncio.sleep(sleep_time)
        print(f"AsyncConcreteObserverA received message: {message}")

class AsyncConcreteObserverB(IAsyncObserver):
    async def update(self, message):
        sleep_time = random.uniform(0.5, 2.0)  # Random sleep time between 0.5 and 2.0 seconds
        await asyncio.sleep(sleep_time)
        print(f"AsyncConcreteObserverB received message: {message}")
