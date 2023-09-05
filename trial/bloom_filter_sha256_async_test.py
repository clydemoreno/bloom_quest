import unittest

import sys
import asyncio
import pytest
from bloom_filter_sha256 import BloomFilter


sys.path.append("./reader")
from bloom_filter_reader import BloomFilterReader

class TestAsyncConcreteSubject(unittest.IsolatedAsyncioTestCase):

    @pytest.mark.asyncio
    async def test_async_concrete_subject(self):
        subject = BloomFilterReader()
        observer_a = BloomFilter(100, 0.01)

        await subject.attach(observer_a)

        tasks = []

        message = f"Load array"
        task_a = asyncio.create_task(subject.notify(message))
        tasks.append(task_a)
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    pytest.main([__file__])