import sys
sys.path.append("../messaging")
from IAsyncSubject import IAsyncSubject

import asyncio

class BloomFilterReader(IAsyncSubject):
    # def __init__(self):
    #     self._observers = []

    # async def attach(self, observer):
    #     if observer not in self._observers:
    #         self._observers.append(observer)

    # async def detach(self, observer):
    #     self._observers.remove(observer)

    async def notify(self, message):
        for observer in self._observers:
            await asyncio.gather(*(observer.update(message) for observer in self._observers))




# from IAsyncSubject import IAsyncSubject
# import asyncio

# class AsyncConcreteSubject(IAsyncSubject):
    # async def notify(self, message):
    #     await asyncio.gather(*(observer.update(message) for observer in self._observers))