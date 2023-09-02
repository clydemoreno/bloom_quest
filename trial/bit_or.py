import random
def bitwise_or(bit_array1, bit_array2):
    result = []
    for bit1, bit2 in zip(bit_array1, bit_array2):
        result.append(bit1 | bit2)
    return result

def generate_random_bit_array(size):
    bit_array = [random.choice([0, 1]) for _ in range(size)]
    return bit_array
