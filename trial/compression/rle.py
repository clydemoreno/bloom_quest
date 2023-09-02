import time
import numpy as np

def rle_encode(data):
    encoded_data = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data.append(str(count))
            encoded_data.append(data[i - 1])
            count = 1
    encoded_data.append(str(count))
    encoded_data.append(data[-1])
    return ''.join(encoded_data)

def rle_decode(encoded_data):
    decoded_data = []
    i = 0
    while i < len(encoded_data):
        count = int(encoded_data[i])
        symbol = encoded_data[i + 1]
        decoded_data.extend([symbol] * count)
        i += 2
    return np.array(decoded_data)

# Generate random bit array using NumPy
data_size = 100000
random_bits = np.random.randint(2, size=data_size, dtype=np.uint8)

# Convert random bits to a NumPy array of strings ("0" or "1")
data = np.array(["0" if bit == 0 else "1" for bit in random_bits])

# Measure execution time using time module
start_time = time.time()

# Encode using RLE
encoded_data = rle_encode(data)

encoding_time = time.time() - start_time

# Calculate compressed size
compressed_size = len(encoded_data) / 8  # bytes

# Print results
print("Original size:", len(data), "bits")
print("Compressed size:", compressed_size, "bytes")
print("Compression ratio:", len(data) / compressed_size)
print("Encoding time:", encoding_time, "seconds")

# Decode using RLE
decoded_data = rle_decode(encoded_data)

# Convert decoded data back to a NumPy array of strings ("0" or "1")
decoded_data_array = np.array([bit for bit in decoded_data])

# Check if decoded data matches the original input data
print("Decoded data matches input data:", np.array_equal(random_bits, decoded_data_array))
