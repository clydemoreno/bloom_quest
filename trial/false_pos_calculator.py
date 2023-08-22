import random
def calc_false_positive(bit_size:int, number_of_items:int, num_of_hashes: int):
    prob = 1 - (1 - 1/bit_size) ** (num_of_hashes * number_of_items)
    return prob


def simulate(num_simulations: int, num_of_items: int, bit_size:int) -> float:
    count = 0
    for _ in range(num_simulations):
        bit_array = [ random.randint(1,num_of_items)  for _ in range(num_of_items) ]
        if len(bit_array) != len(set(bit_array)):
            count += 1
    return count/num_simulations


print(f"Prob: {calc_false_positive(365, 10, 1)}")
print(f"Simulated Prob: {simulate(10000, 365, 1)}")