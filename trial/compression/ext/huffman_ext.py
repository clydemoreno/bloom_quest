import sys

# Remove current directory from sys.path
if '' in sys.path:
    sys.path.remove('')
from huffman import encode, decode

# Your data as a list of symbols (e.g., ['A', 'B', 'C', ...])
data = ['A', 'B', 'C', 'A', 'B', 'A', 'A']

# Encode the data using Huffman coding
encoded_data, codebook = encode(data)

# Decode the encoded data using Huffman coding
decoded_data = decode(encoded_data, codebook)

print("Original data:", data)
print("Encoded data:", encoded_data)
print("Decoded data:", decoded_data)
