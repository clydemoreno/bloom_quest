from abc import ABC, abstractmethod

class IAsyncObserver(ABC):
    @abstractmethod
    async def update(self, message):
        pass


