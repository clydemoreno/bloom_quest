import random

class BloomFilter():
    def __init__(self, num_of_items:int, fp_prob):
        self.size = num_of_items
        self.bitarray = [False]  * self.size
        self.fp_prob = fp_prob

    def add(self,id: str):
        if isinstance(id,str ):
            item = int(id)
        else:
             item = id
        index = item % self.size
        self.bitarray[index] = True

    def check(self, id:str):
        index = int(id) % self.size
        return self.bitarray[index]
    
    def get_size(self, n, p):
        return self.size

    def get_hash_count(self, m, n):
        return 1
    

if __name__ == "__main__":
    expected_elements = 10
    true_elements = [str(random.randint(1, 10)) for _ in range(expected_elements  ) ]
    false_elements = [str(random.randint(11, 2000)) for _ in range(expected_elements) ]
    query_elements = true_elements + false_elements

    bf = BloomFilter(expected_elements, 0.01)

    print (type(true_elements[0]))
    for element in true_elements:
        print("true el", element)
        bf.add(element)

    for i in range(1,30):
        print(i)
        bf.add(i)


    print(bf.check(10))
    print(bf.check(20))
    print(bf.check(2))
    print(bf.check("10"))





