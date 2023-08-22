import random
def simulate_calculation(num_simulations, num_birthdays):
    count = 0
    for _ in range(num_simulations):
        birthdays = random.sample(range(1, 366), num_birthdays)
        for i in range(num_birthdays - 2):  # Adjusted range to accommodate 3 consecutive
            if all(birthdays[j] % 7 == 1 for j in range(i, i + 3)):
                count += 1
                break
    return count / num_simulations

num_simulations = 1000000  # Number of simulations
num_birthdays = 20         # Number of birthdays

probability = simulate_calculation(num_simulations, num_birthdays)
print("Approximate probability (simulation):", probability)