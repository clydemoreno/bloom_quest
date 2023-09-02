import unittest
from IObserver import ConcreteObserverA, ConcreteObserverB, ConcreteSubject

class TestObserverPattern(unittest.TestCase):
    def test_observer_pattern(self):
        observerA = ConcreteObserverA()
        observerB = ConcreteObserverB()

        subject = ConcreteSubject()
        subject.attach(observerA)
        subject.attach(observerB)

        # Test that observers receive notifications
        with self.assertLogs() as cm:
            subject.notify("Hello, observers!")
        self.assertIn("ConcreteObserverA received message: Hello, observers!", cm.output)
        self.assertIn("ConcreteObserverB received message: Hello, observers!", cm.output)

        # Detach observerB and test again
        subject.detach(observerB)
        with self.assertLogs() as cm:
            subject.notify("Goodbye, observerB!")
        self.assertIn("ConcreteObserverA received message: Goodbye, observerB!", cm.output)
        self.assertNotIn("ConcreteObserverB received message: Goodbye, observerB!", cm.output)

if __name__ == "__main__":
    unittest.main()
