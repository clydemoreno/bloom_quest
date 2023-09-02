import heapq
from collections import defaultdict
import time
import numpy as np

class HuffmanNode:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):  # Added comparison method for heapq
        return self.frequency < other.frequency

def build_frequency_table(data):
    frequency_table = defaultdict(int)
    for symbol in data:
        frequency_table[symbol] += 1
    return frequency_table

def build_huffman_tree(frequency_table):
    priority_queue = [HuffmanNode(symbol, freq) for symbol, freq in frequency_table.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left_node = heapq.heappop(priority_queue)
        right_node = heapq.heappop(priority_queue)

        combined_frequency = left_node.frequency + right_node.frequency
        combined_node = HuffmanNode(None, combined_frequency)
        combined_node.left = left_node
        combined_node.right = right_node

        heapq.heappush(priority_queue, combined_node)

    return priority_queue[0]

def build_huffman_codes(huffman_tree):
    codes = {}
    def traverse(node, code):
        if node.symbol is not None:
            codes[node.symbol] = code
            return
        if node.left:
            traverse(node.left, code + "0")
        if node.right:
            traverse(node.right, code + "1")
    traverse(huffman_tree, "")
    return codes

def huffman_encode(data, huffman_codes):
    encoded_data_list = []
    current_byte = 0
    num_bits = 0

    for symbol in data:
        code = huffman_codes[symbol]
        for bit in code:
            current_byte |= (int(bit) << num_bits)
            num_bits += 1

            if num_bits == 8:
                encoded_data_list.append(current_byte)
                current_byte = 0
                num_bits = 0

    if num_bits > 0:
        encoded_data_list.append(current_byte)

    return bytes(encoded_data_list)

def huffman_decode(encoded_data, huffman_tree):
    decoded_data = np.empty(len(encoded_data) * 8, dtype=np.uint8)  # Allocate enough space for bits
    decoded_index = 0
    node = huffman_tree
    for byte in encoded_data:
        for bit_num in range(8):
            bit = (byte >> bit_num) & 1
            if bit == 0:
                node = node.left
            else:
                node = node.right
            if node.symbol is not None:
                decoded_data[decoded_index] = int(node.symbol)
                decoded_index += 1
                node = huffman_tree
    return decoded_data[:decoded_index]


# Generate random bit array using NumPy
data_size = 1000000
random_bits = np.random.randint(2, size=data_size, dtype=np.uint8)

# Convert random bits to a NumPy array of bytes (0 or 1)
data_bytes = random_bits.tobytes()

# Measure execution time using time module
start_time = time.time()

# Encode
frequency_table = build_frequency_table(data_bytes)
huffman_tree = build_huffman_tree(frequency_table)
huffman_codes = build_huffman_codes(huffman_tree)
encoded_data = huffman_encode(data_bytes, huffman_codes)

# Calculate compressed size
compressed_size = len(encoded_data)  # bytes

encoding_time = time.time() - start_time

# Print results
print("Original size:", len(data_bytes), "bytes")
print("Compressed size:", compressed_size, "bytes")
print("Compression ratio:", len(data_bytes) / compressed_size)
print("Encoding time:", encoding_time, "seconds")

# Decode
decoded_data = huffman_decode(encoded_data, huffman_tree)

# Calculate the expected length of the decoded data in bytes
expected_decoded_length = (len(data_bytes) * 8 + 7) // 8

# Convert decoded data back to a NumPy array of bytes (0 or 1)
decoded_data_bytes = np.packbits(decoded_data)

# Truncate decoded data to match expected length
decoded_data_bytes = decoded_data_bytes[:expected_decoded_length]

# Check if decoded data matches the original input data
print("Decoded data matches input data:", np.array_equal(data_bytes, decoded_data_bytes))

print("Decoded data:", decoded_data)
