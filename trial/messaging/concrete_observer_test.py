import unittest
from concrete_observers import ConcreteObserverA, ConcreteObserverB
from concrete_subject import ConcreteSubject

class TestObserverPattern(unittest.TestCase):
    def test_observer_pattern(self):
        observerA = ConcreteObserverA()
        observerB = ConcreteObserverB()

        subject = ConcreteSubject()
        subject.attach(observerA)
        subject.attach(observerB)

        # Test that observers receive notifications
        subject.notify("Hello, observers!")

        # Detach observerB and test again
        subject.detach(observerB)
        subject.notify("Goodbye, observerB!")

if __name__ == "__main__":
    unittest.main()
