from abc import ABC, abstractmethod

class IAsyncObserver(ABC):
    @abstractmethod
    async def update(self, message):
        pass

class IAsyncSubject(ABC):
    def __init__(self, max_observers=10):
        self._max_observers = max_observers
        self._observers = []

    async def attach(self, observer):
        if len(self._observers) < self._max_observers:
            if observer not in self._observers:
                self._observers.append(observer)
        else:
            print("Cannot attach more observers. Max limit reached.")

    async def detach(self, observer):
        self._observers.remove(observer)

    @abstractmethod
    async def notify(self, message):
        pass
