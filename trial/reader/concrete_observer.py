class Observer:
    def update(self, message):
        pass

class ConcreteObserver(Observer):
    def update(self, message):
        print(f"ConcreteObserver received message: {message}")
