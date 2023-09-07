import unittest
import asyncio
import sys
import io
import contextlib

from pathlib import Path
parent_dir = Path(__file__).resolve().parent
print ("parent_dir: ", parent_dir.parent)
# sys.path.append("../messaging")
# Add the 'messaging' directory to sys.path
parent_of_parent = parent_dir.parent
sys.path.append(str(parent_of_parent / 'messaging'))

# from IAsyncSubject import IAsyncSubject

sys.path.append(str(parent_of_parent))

from utility.load_config import load_config


from IAsyncSubject import IAsyncSubject

from concrete_async_observers import AsyncConcreteObserverA, AsyncConcreteObserverB

from bloom_filter_reader import BloomFilterReader

import time


class TestAsyncConcreteSubject(unittest.IsolatedAsyncioTestCase):
    async def test_async_concrete_subject(self):
        config_data = load_config()
        folder_path = str (parent_of_parent / config_data["data"]["path"])
        print ("folder to watch: ", folder_path)
        subject = BloomFilterReader(folder_path)
        observer_a = AsyncConcreteObserverA()
        observer_b = AsyncConcreteObserverB()

        # Capture printed output
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            await subject.attach(observer_a)
            await subject.attach(observer_b)

            num_iterations = 5

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

        # Check if the captured output contains the expected messages
        captured_output.seek(0)
        output_lines = captured_output.read().splitlines()

        # Check for messages from both observers
        for i in range(num_iterations):
            expected_message_a = f"AsyncConcreteObserverA received message: Message iteration {i + 1}"
            expected_message_b = f"AsyncConcreteObserverB received message: Message iteration {i + 1}"
            self.assertIn(expected_message_a, output_lines)
            self.assertIn(expected_message_b, output_lines)

        # Check for the "Goodbye, observer B!" message
        self.assertIn("AsyncConcreteObserverA received message: Goodbye, observer B!", output_lines)

if __name__ == "__main__":
    unittest.main()
