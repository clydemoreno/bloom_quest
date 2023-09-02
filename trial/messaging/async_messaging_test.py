import unittest
import asyncio
from concrete_async_observers import AsyncConcreteObserverA, AsyncConcreteObserverB
from concrete_async_subject import AsyncConcreteSubject
import time

class TestAsyncConcreteObserver(unittest.IsolatedAsyncioTestCase):
    async def test_async_concrete_observer_a(self):
        observer_a = AsyncConcreteObserverA()
        await observer_a.update("Hello from TestAsyncConcreteObserver!")

    async def test_async_concrete_observer_b(self):
        observer_b = AsyncConcreteObserverB()
        await observer_b.update("Hello from TestAsyncConcreteObserver!")

class TestAsyncConcreteSubject(unittest.IsolatedAsyncioTestCase):
    async def test_async_concrete_subject(self):
        subject = AsyncConcreteSubject()
        observer_a = AsyncConcreteObserverA()
        observer_b = AsyncConcreteObserverB()

        await subject.attach(observer_a)
        await subject.attach(observer_b)

        num_iterations = 5
        start_time = time.time()

        tasks = []

        for i in range(num_iterations):
            message = f"Message iteration {i + 1}"
            task_a = asyncio.create_task(subject.notify(message))
            task_b = asyncio.create_task(observer_b.update(message))
            tasks.append(task_a)
            tasks.append(task_b)

        await asyncio.gather(*tasks)

        await subject.detach(observer_b)
        await subject.notify("Goodbye, observer B!")


        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"TestAsyncConcreteSubject (without asyncio.create_task()) took {elapsed_time:.2f} seconds")



class TestSyncConcreteSubjectWithoutCreateTask(unittest.IsolatedAsyncioTestCase):
    async def test_async_concrete_subject(self):
        subject = AsyncConcreteSubject()
        observer_a = AsyncConcreteObserverA()
        observer_b = AsyncConcreteObserverB()

        await subject.attach(observer_a)
        await subject.attach(observer_b)

        num_iterations = 5
        start_time = time.time()

        for i in range(num_iterations):
            message = f"Message iteration {i + 1}"
            await subject.notify(message)
            await asyncio.sleep(1.0)  # Simulate asynchronous processing

        await subject.detach(observer_b)
        await subject.notify("Goodbye, observer B!")        


if __name__ == "__main__":
    unittest.main()
