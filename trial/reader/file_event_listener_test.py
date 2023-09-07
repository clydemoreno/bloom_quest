import unittest
import tempfile
import time
import os
from watchdog.observers import Observer
from pathlib import Path
from file_event_listener import EventHandler  

class TestEventHandler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.file_path = self.temp_dir / "test.txt"

    def tearDown(self):
        for path in self.temp_dir.iterdir():
            if path.is_file():
                path.unlink()
        self.temp_dir.rmdir()

    def test_on_created_callback(self):
        def callback(src_path):
            self.callback_called = True
            src_path = Path(src_path).resolve()  # Normalize the path
            self.assertEqual(src_path, self.file_path.resolve())

        self.callback_called = False

        event_handler = EventHandler(str(self.temp_dir),callback)

        # Create a test file
        with self.file_path.open("w") as f:
            f.write("Test content")

        # Wait for the event to be processed
        time.sleep(2)

        # Check if the callback was called
        self.assertTrue(self.callback_called)

        event_handler.file_observer.stop()
        event_handler.file_observer.join()


if __name__ == "__main__":
    unittest.main()
