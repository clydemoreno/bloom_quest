import asyncio

class AsyncFile:
    def __init__(self, file_path, mode):
        self.file_path = file_path
        self.mode = mode

    async def __aenter__(self):
        self.file = await asyncio.to_thread(open, self.file_path, self.mode)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await asyncio.to_thread(self.file.close)

    async def read(self):
        return await asyncio.to_thread(self.file.read)

async def main():
    async with AsyncFile('test_file.txt', 'r') as file:
        content = await file.read()
        print(content)

if __name__ == "__main__":
    asyncio.run(main())
