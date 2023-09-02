import numpy as np
import gmpy2


def counting_compression(data):
    compressed_data = ""
    count = 0
    current_bit = data[0]

    for bit in data:
        if bit == current_bit:
            count += 1
        else:
            compressed_data += str(count)
            count = 1
            current_bit = bit

    compressed_data += str(count)  # Add count of the last bit
    return compressed_data


def counting_decompression(compressed_data):
    decompressed_data = np.array([], dtype=np.uint8)
    i = 0
    while i < len(compressed_data):
        count_str = ""
        while i < len(compressed_data) and compressed_data[i].isdigit():
            count_str += compressed_data[i]
            i += 1
        count = gmpy2.mpz(count_str)
        bit = 0 if len(decompressed_data) % 2 == 0 else 1
        decompressed_data = np.concatenate((decompressed_data, np.full(int(count), bit, dtype=np.uint8)))

    return decompressed_data

# Generate random uint8 data using NumPy
data_size = 100000
random_data = np.random.randint(2, size=data_size, dtype=np.uint8)

# Perform counting compression
compressed_data = counting_compression(random_data)

# Perform counting decompression
decompressed_data = counting_decompression(compressed_data)

# Check if decompressed data matches the original input
print("Original data matches decompressed data:", np.array_equal(random_data, decompressed_data))
