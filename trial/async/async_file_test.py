from async_file import AsyncFile

import unittest
import asyncio
import tempfile  # Import tempfile to create a temporary directory

class TestAsyncFile(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a temporary directory and file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = open(self.temp_dir.name + '/test_file.txt', 'w')
        self.test_file.write('Hello, World!')
        self.test_file.close()

    def tearDown(self):
        # Clean up the temporary directory and file
        self.temp_dir.cleanup()
        pass

    async def test_read(self):
        async with AsyncFile(self.temp_dir.name + '/test_file.txt', 'r') as file:
            content = await file.read()
            self.assertEqual(content, 'Hello, World!')

    async def test_write(self):
        async with AsyncFile(self.temp_dir.name + '/test_file.txt', 'w') as file:
            await file.write('This is a test.')

        # Verify that the file was written correctly
        with open(self.temp_dir.name + '/test_file.txt', 'r') as file:
            content = file.read()
            self.assertEqual(content, 'This is a test.')

    async def test_context_management(self):
        async with AsyncFile(self.temp_dir.name + '/test_file.txt', 'w') as file:
            # Do some operations within the context
            await file.write('Test content.')

        # Verify that the file was closed properly
        with self.assertRaises(FileNotFoundError):
            with open(self.temp_dir.name + '/no_file_this_name.txt', 'r'):
                pass

if __name__ == '__main__':
    unittest.main()
