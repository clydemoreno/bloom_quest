from observer import IAsyncObserver, IAsyncSubject

class ComplexObject(IAsyncObserver, IAsyncSubject):
    def __init__(self, observer_instance, subject_instance):
        super().__init__()  # Initialize the base classes
        self._observers = []
        self._observer_instance = observer_instance
        self._subject_instance = subject_instance

    async def update(self, message):
        await asyncio.sleep(1)  # Simulate asynchronous processing
        print(f"ComplexObject received message: {message}")

    async def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    async def detach(self, observer):
        self._observers.remove(observer)

    async def notify(self, message):
        for observer in self._observers:
            await observer.update(message)

    def perform_complex_operation(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._perform_complex_operation())

    async def _perform_complex_operation(self):
        await self._observer_instance.update("ComplexObject performing a complex operation")
        await self._subject_instance.notify("ComplexObject performing a complex operation")
