import asyncio

async def async_file_io_task(task_id):
    async with open('test_file.txt', 'r') as file:
        content = await file.read()
        print(f"Async Task {task_id}: Read content: {content.strip()}")

async def main():
    tasks = [async_file_io_task(i) for i in range(10)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
