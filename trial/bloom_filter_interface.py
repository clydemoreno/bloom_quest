
class IBloomFilter:
    @property
    def size(self):
        if hasattr(self.filter, 'size'):
            return self.filter.size

    @property
    def fp_prob(self):
        if hasattr(self.filter, 'fp_prob'):
            return self.filter.fp_prob

    @property
    def hash_count(self):
        if hasattr(self.filter, 'hash_count'):
            return self.filter.hash_count

    def __init__(self, implementation):
        self.filter = implementation

    def add(self, item):
        self.filter.add(item)

    def check(self, item):
        # return self.filter.check(item)
        if hasattr(self.filter, 'check'):
            return self.filter.check(item)
        elif hasattr(self.filter, 'query'):
            return self.filter.query(item)
        else:
            raise AttributeError("No suitable method found in the Bloom Filter implementation")
        
    def get_size(self, n, p):
        return self.filter.get_size(n,p)

    def get_hash_count(self, m, n):
        return self.filter.get_hash_count(m,n)


# # Create instances of different Bloom Filter implementations
# original_filter = IBloomFilter(BloomFilter(items_count=1000, fp_prob=0.01))
# # another_filter = BloomFilterWrapper(AnotherBloomFilter(items_count=500, fp_prob=0.05))

# # Use the wrapper methods with different implementations
# items_to_add = ["apple", "banana", "cherry"]
# for item in items_to_add:
#     original_filter.add(item)
#     another_filter.add(item)

# items_to_check = ["apple", "blueberry", "cherry"]
# for item in items_to_check:
#     if original_filter.check(item):
#         print(f"{item} might be in the original filter.")
#     if another_filter.check(item):
#         print(f"{item} might be in the another filter.")
