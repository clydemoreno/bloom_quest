from IObserver import IObserver

class ConcreteObserverA(IObserver):
    def update(self, message):
        print(f"ConcreteObserverA received message: {message}")

class ConcreteObserverB(IObserver):
    def update(self, message):
        print(f"ConcreteObserverB received message: {message}")
