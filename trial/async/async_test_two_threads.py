import asyncio
import threading

# Shared counter for completed iterations
completed_iterations_async = 0
completed_iterations_sync = 0

# Synchronization mechanisms
async_event = asyncio.Event()
lock = threading.Lock()

# Asynchronous file I/O thread
async def async_io_thread():
    global completed_iterations_async
    async with lock:
        async with open('test_file.txt', 'r') as file:
            content = await file.read()
            completed_iterations_async += 1
            async_event.set()

# Synchronous file I/O thread
def sync_io_thread():
    global completed_iterations_sync
    with lock:
        with open('test_file.txt', 'r') as file:
            content = file.read()
            completed_iterations_sync += 1

# Stress testing function
async def stress_test():
    async_tasks = [async_io_thread() for _ in range(10)]
    sync_threads = [threading.Thread(target=sync_io_thread) for _ in range(10)]

    # Start asynchronous tasks
    for task in async_tasks:
        asyncio.create_task(task)

    # Start synchronous threads
    for thread in sync_threads:
        thread.start()

    # Wait for all asynchronous tasks to complete
    await asyncio.gather(*async_tasks)

    # Wait for all synchronous threads to complete
    for thread in sync_threads:
        thread.join()

if __name__ == "__main__":
    asyncio.run(stress_test())
    print("Async completed iterations:", completed_iterations_async)
    print("Sync completed iterations:", completed_iterations_sync)
