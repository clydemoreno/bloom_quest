import unittest
from bloom_filter_sha256 import BloomFilter
from murmur_hash import murmur_hash

class TestBloomFilter(unittest.TestCase):
    
    def test_add_and_check(self):
        # Initialize a BloomFilter with an expected false positive rate of 1%
        #todo:  fix this. 
        hash_list = [None , _murmur_hash]

        for h in hash_list:
            bloom_filter = BloomFilter(100, 0.01,hash_function=h)

            # Add words to the BloomFilter
            words = ["apple", "banana", "cherry", "date", "elderberry"]
            for word in words:
                bloom_filter.add(word)

            # Check if the added words are in the filter (may return false positives)
            for word in words:
                self.assertTrue(bloom_filter.check(word))

            # Check if words that weren't added return False
            self.assertFalse(bloom_filter.check("grape"))
            self.assertFalse(bloom_filter.check("fig"))
            self.assertTrue(bloom_filter.check("apple"))
            self.assertTrue(bloom_filter.check("elderberry"))
    

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


def _hash( item, seed):
    return hash(item + str(seed)) 


def _murmur_hash( item, seed):
    input_bytes = item.encode('utf-8')  # Convert the string to bytes

    return murmur_hash(input_bytes, str(seed)) 



if __name__ == '__main__':
    unittest.main()
