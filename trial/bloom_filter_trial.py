import array
import sys
import random
import time
import hash

def naive_hash(input_str:str, slot:int):
    num = convert_to_number(input_str)
    return num % slot

def custom_hash(input_str: str, seed: int):
    hash_value = seed
    for char in input_str:
        # 31 move the bits to 5, also a prime number
        hash_value = (hash_value * 31) + ord(char) # combine hashvalue with ASCII
    
    return hash_value


def custom_hash_by_shifting(input_str: str, seed: int):
    hash_value = seed
    for char in input_str:
        # 31 move the bits to 5, also a prime number
        hash_value = (hash_value << 5) - hash_value + ord(char)
    
    return hash_value



def simulate_calculation(num_simulations, num_birthdays):
    count = 0
    for _ in range(num_simulations):
        birthdays = random.sample(range(1, 366), num_birthdays)
        for i in range(num_birthdays - 1):
            if birthdays[i] % 7 == 1 and birthdays[i+1] % 7 == 1:
                count += 1
                break
    return count / num_simulations

num_simulations = 1000000  # Number of simulations
num_birthdays = 10         # Number of birthdays



# there are 365 possible combinations
# 7 distinct buckets or day
# 7 / 365


def calculate_probability(key_space:int, slot:int, consecutive: int, n:int) -> float:
    remaining =  key_space - slot
    probability = 0
    while n > 0:
        probability += ((slot/key_space) ** consecutive) * ((remaining/key_space) ** (n - consecutive))
        n-=1
    return probability


def simulate(num_simulations: int, num_birthdays: int) -> float:
    count = 0
    for _ in range(num_simulations):
        birthday_array = [ random.randint(1,365)  for _ in range(num_birthdays) ]
        if len(birthday_array) != len(set(birthday_array)):
            count += 1
    return count/num_simulations



def simulate_day_prob(num_simulations: int, num_birthdays: int) -> float:
    count = 0
    for _ in range(num_simulations):
        birthday_array = [ random.randint(1,365) % 7 for _ in range(num_birthdays) ]
        if len(birthday_array) != len(set(birthday_array)):
            count += 1
    print(f"count/simulations: {count}, {num_simulations}, {birthday_array} ")
    return float(count/num_simulations)


def convert_bitarray_to_number(arr:array) -> int:
    bit_string = ''.join(str(bit) for bit in arr)
    integer_number = int(bit_string,2)
    return integer_number

def convert_to_number(id: str) -> int:

    number = ""
    for c in id:
        if c.isdigit():
            # print(ord('0') , ord(c) -  ord('0') , c)
            number += str(ord(c) -  ord('0') )
        else:
            # print(ord('a') , ord(c) -  ord('a') , c)
            number += str(ord(c) -  ord('a') )

    # print (number, int(number))
    return int(number)


if __name__ == '__main__':
    print("occurances out of 365 possible combos")
    print(f"Simulated Prob 10 occurances : {simulate(10000,10)}")
    print(f"Simulated Prob 20 occurances: {simulate(10000,20)}")
    print(f"Simulated Prob 30 occurances: {simulate(10000,30)}")

    print("occurences out of 7 slots out of 365 possible combos")

    print(f"Simulated Prob  10 occurences: {simulate_day_prob(10000,10)}")
    print(f"Simulated Prob  20 occurences: {simulate_day_prob(10000,20)}")
    print(f"Simulated Prob  30 occurences: {simulate_day_prob(10000,30)}")

    


    key_space = 7
    slot = 1
    remaining =  key_space - slot
    consecutive = 2
    n = 10

    print(f"Prob: {calculate_probability(key_space,slot,consecutive,n)}")


    key_space = 100
    slot = 7
    consecutive = 2
    n = 10

    print(f"Prob: ks:  slot: 7 100 {calculate_probability(key_space,slot,consecutive,n)}")


    key_space = 365
    slot = 7
    consecutive = 1
    n = 10

    print(f"Prob: ks: 365 slot: 7 {calculate_probability(key_space,slot,consecutive,n)}")


    key_space = 10000
    slot = 400
    ratio = slot/key_space
    consecutive = 1
    n = 10

    print(f"Prob: ks: 10000 slot: 7 ratio:  {ratio} consecutive:{consecutive} {calculate_probability(key_space,slot,consecutive,n)}")


    key_space = 10000
    slot = 400
    ratio = slot/key_space
    consecutive = 2
    n = 10

    print(f"Prob: ks: 10000 slot: 7 ratio: {ratio} consecutive:{consecutive} {calculate_probability(key_space,slot,consecutive,n)}")


    key_space = 1000000
    slot = 20000
    ratio = slot/key_space
    consecutive = 3
    n = 10

    print(f"Prob: ks: 10000 slot: 7 ratio: {ratio} consecutive:{consecutive} {calculate_probability(key_space,slot,consecutive,n)}")


    #for 175 M possible IDs
    # you can have a size of 12




    probability = simulate_calculation(num_simulations, num_birthdays)
    print("Approximate probability (simulation):", probability)

    # hash = custom_hash("9874", 1)
    # print(f"hash: {hash}")

    # hash = custom_hash("9874", 2)
    # print(f"hash: {hash}")

    input_string = "9874"
    seeds = [1, 2, 3]

    # for seed in seeds:
    #     start_time = time.time()
    #     result = custom_hash(input_string, seed)
    #     end_time = time.time()
    #     execution_time = end_time - start_time

    #     print(f"Hash result for seed {seed}: {result}")
    #     print(f"Execution time for seed {seed}: {execution_time:.6f} seconds\n")


    # for seed in seeds:
        
    #     start_time = time.time()
    #     result = custom_hash_by_shifting(input_string, seed)
    #     end_time = time.time()
    #     execution_time = end_time - start_time

    #     print(f"Hash result for seed {seed}: {result}")
    #     print(f"Execution time for seed {seed}: {execution_time:.6f} seconds\n")


    # day = [(random.randint(1,365) % 7 ) for _ in range(10)]
    # print (day)

def run_this():

    arr = ["pgo9874","pgo7865","pgo5641","pgo9870","pgo7698","pgo0987"]


    #create an array of 'b' type to store 1 or 0
    bit_array = array.array('b', [0] * 175760000)
    integer_number = convert_bitarray_to_number(bit_array)

    memory_usage = sys.getsizeof(bit_array)
    print(f"memory_usage: {memory_usage} bytes")


    keyspace = 26 * 26 * 26 * 10 * 10 * 10 * 10

    # print("keyspace",keyspace)
    n = keyspace



    for s in arr:
        hash = convert_to_number(s) % n
        print(convert_to_number(s), n, convert_to_number(s) % n )
        bit_array[hash ] = 1

    integer_number = convert_bitarray_to_number(bit_array)


    memory_usage = sys.getsizeof(bit_array)
    print(f"memory_usage: {memory_usage} bytes, integer number: {integer_number}")




    arr2 = ["pgo9874","pgo2865","pgo1641","pgo9870","pgo7698","pgo0987"]

    res = []
    for s in arr2:
        hash = convert_to_number(s) % n
        res.append(bit_array[hash])

    print(f"result: {res}")








# 101001000111011000100000000