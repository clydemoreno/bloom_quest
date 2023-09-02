from observer import Observer

class ConcreteObserverA(Observer):
    def update(self, message):
        print(f"ConcreteObserverA received message: {message}")

class ConcreteObserverB(Observer):
    def update(self, message):
        print(f"ConcreteObserverB received message: {message}")
