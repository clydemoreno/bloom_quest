import random
import string

# Generate random test data with random characters in the name
def generate_test_data(num_rows):
    data = []
    for i in range(1, num_rows + 1):
        random_chars = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(5))  # Generate 5 random characters
        order_name = f"Order_{i}_{random_chars}"
        data.append((order_name,))
    return data

# Number of rows in the table
num_rows = 5000

# Generate test data
test_data = generate_test_data(num_rows)

# Print the first few rows of test data
for i in range(min(10, num_rows)):
    print(test_data[i])
