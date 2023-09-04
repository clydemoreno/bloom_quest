
from abc import ABC, abstractmethod

class IObserver(ABC):
    @abstractmethod
    def update(self, message):
        pass

class ISubject(ABC):
    @abstractmethod
    def attach(self, observer):
        pass
     
    @abstractmethod
    def detach(self, observer):
        pass
    
    @abstractmethod
    def notify(self, message):
        pass
