from IAsyncSubject import IAsyncSubject
import asyncio

class AsyncConcreteSubject(IAsyncSubject):
    async def notify(self, message):
        await asyncio.gather(*(observer.update(message) for observer in self._observers))
