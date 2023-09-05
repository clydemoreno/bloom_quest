import asyncio
from pathlib import Path

class AsyncFile:
    def __init__(self, file_path, mode):
        # Use pathlib.Path to create a Path object for the relative file path
        self.file_path = Path(file_path)
        self.mode = mode

    async def __aenter__(self):
        # Use the resolved path to open the file
        self.file = await asyncio.to_thread(open, self.file_path.resolve(), self.mode)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await asyncio.to_thread(self.file.close)

    async def read(self):
        return await asyncio.to_thread(self.file.read)

    async def write(self, data):
        return await asyncio.to_thread(self.file.write, data)

# async def main():
#     # Example usage with a relative file path
#     async with AsyncFile('./test_file.txt', 'r') as file:
#         content = await file.read()
#         print(content)

# if __name__ == "__main__":
#     asyncio.run(main())
