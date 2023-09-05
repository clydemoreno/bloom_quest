import unittest
from bloom_filter_sha256 import BloomFilter
from murmur_hash import murmur_hash
import sys
sys.path.append("./reader")
from bloom_filter_reader import BloomFilterReader

def _hash( item, seed):
    return hash(item + str(seed)) 


def _murmur_hash( item, seed):
    return  murmur_hash(item, seed) 


class TestBloomFilter(unittest.TestCase):
    
    def test_add_and_check(self):
        # Initialize a BloomFilter with an expected false positive rate of 1%
        #todo:  fix this. 
        hash_list = [None]

        for h in hash_list:
            bloom_filter = BloomFilter(100, 0.01,hash_function=h)

            # Add words to the BloomFilter
            words = ["apple", "banana", "cherry", "date", "elderberry"]
            for word in words:
                bloom_filter.add(word)

            words = [1, 2,3, 4, 5]
            for word in words:
                bloom_filter.add(str(word))

            # Check if the added words are in the filter (may return false positives)
            for word in words:
                self.assertTrue(bloom_filter.check(word))

            # Check if words that weren't added return False
            self.assertFalse(bloom_filter.check("grape"))
            self.assertFalse(bloom_filter.check("fig"))
            self.assertTrue(bloom_filter.check("apple"))
            self.assertTrue(bloom_filter.check("elderberry"))
    


    async def test_async_concrete_subject(self):
        subject = BloomFilterReader()
        # observer_a = BloomFilter(100, 0.01)

        # await subject.attach(observer_a)

        # tasks = []

        # message = f"Load array"
        # task_a = asyncio.create_task(subject.notify(message))
        # tasks.append(task_a)
        # await asyncio.gather(*tasks)





    # def test_add_and_check(self):
    #     # Initialize a BloomFilter with an expected false positive rate of 1%
    #     bloom_filter = BloomFilter(100, 0.01)

    #     # Add words to the BloomFilter
    #     words = ["apple", "banana", "cherry", "date", "elderberry"]
    #     for word in words:
    #         bloom_filter.add(word)

    #     # Check if the added words are in the filter (may return false positives)
    #     for word in words:
    #         self.assertTrue(bloom_filter.check(word))

    #     # Check if words that weren't added return False
    #     self.assertFalse(bloom_filter.check("grape"))
    #     self.assertFalse(bloom_filter.check("fig"))
    #     self.assertTrue(bloom_filter.check("apple"))
    #     self.assertTrue(bloom_filter.check("elderberry"))





if __name__ == '__main__':
    unittest.main()
