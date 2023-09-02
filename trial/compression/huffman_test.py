import time
import numpy as np
from huffman import build_frequency_table, build_huffman_tree, build_huffman_codes, huffman_encode, huffman_decode

# Generate random bit array using NumPy
data_size = 100000
random_bits = np.random.randint(2, size=data_size, dtype=np.uint8)
print(type(random_bits))
# Convert random bits to a NumPy array of strings ("0" or "1")
data = np.array(["0" if bit == 0 else "1" for bit in random_bits])
print(type(data))

# Measure execution time using time module
start_time = time.time()

# Encode
frequency_table = build_frequency_table(data)
huffman_tree = build_huffman_tree(frequency_table)
huffman_codes = build_huffman_codes(huffman_tree)
encoded_data = huffman_encode(data, huffman_codes)

# Store encoded data to a file
with open("./encoded_data.bin", "wb") as encoded_file:
    encoded_file.write(encoded_data)


print("Encoded data has been saved to 'encoded_data.bin'")

# Calculate compressed size
compressed_size = len(encoded_data)  # bytes



encoding_time = time.time() - start_time

# Print results
print("Original size:", len(data), "bytes")
print("Compressed size:", compressed_size, "bytes")
print("Compression ratio:", len(data) / compressed_size)
print("Encoding time:", encoding_time, "seconds")

# Decode
decoded_data = huffman_decode(encoded_data, huffman_tree)

# Convert the decoded data back to integers
decoded_data = np.array([int(bit) for bit in decoded_data], dtype=np.uint8)

# Check if decoded data matches the original input data
print("Decoded data matches input data:", np.array_equal(random_bits, decoded_data))
