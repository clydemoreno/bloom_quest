from observer import Observer, Subject

class ComplexObject(Observer, Subject):
    def __init__(self, observer_instance, subject_instance):
        super().__init__()  # Initialize the base classes
        self._observers = []
        self._observer_instance = observer_instance
        self._subject_instance = subject_instance

    def update(self, message):
        print(f"ComplexObject received message: {message}")

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

    def perform_complex_operation(self):
        # ComplexObject can now interact with both the observer_instance and subject_instance
        self._observer_instance.update("ComplexObject performing a complex operation")
        self._subject_instance.notify("ComplexObject performing a complex operation")
