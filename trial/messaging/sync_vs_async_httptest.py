import asyncio
import time

# Synchronous approach
def fetch_page_sync(url):
    # Simulate fetching a web page synchronously
    time.sleep(2)
    print(f"Fetched page from {url}")

def synchronous_test():
    start_time = time.time()
    urls = ["https://example.com", "https://example.org", "https://example.net"]
    for url in urls:
        fetch_page_sync(url)
    end_time = time.time()
    print(f"Synchronous test took {end_time - start_time:.2f} seconds")

# Asynchronous approach
async def fetch_page_async(url):
    # Simulate fetching a web page asynchronously
    await asyncio.sleep(2)
    print(f"Fetched page from {url}")

async def asynchronous_test():
    start_time = time.time()
    urls = ["https://example.com", "https://example.org", "https://example.net"]
    await asyncio.gather(*(fetch_page_async(url) for url in urls))
    end_time = time.time()
    print(f"Asynchronous test took {end_time - start_time:.2f} seconds")

def main():
    print("Synchronous test:")
    synchronous_test()

    print("\nAsynchronous test:")
    asyncio.run(asynchronous_test())

if __name__ == "__main__":
    main()
