import numpy as np
import gzip
import hashlib
import time

# Suppose you have a NumPy array called 'data'
data_size = 100000
random_bits = np.random.randint(2, size=data_size, dtype=np.uint8)

# Measure the original size
original_size = random_bits.nbytes  # Size in bytes

# Calculate checksum of the original data
checksum_original = hashlib.md5(random_bits).hexdigest()

# Measure execution time for compression and saving
start_time = time.time()

# Compress and save the NumPy array to a gzip-compressed file
with gzip.open('./encoded_data.npy.gz', 'wb') as f_out:
    np.save(f_out, random_bits)

compression_time = time.time() - start_time  # Compression time

# Calculate checksum of the compressed data
with open('encoded_data.npy.gz', 'rb') as f_in:
    compressed_data = f_in.read()
checksum_compressed = hashlib.md5(compressed_data).hexdigest()

# Verify data integrity after compression
data_integrity_verified_compression = (checksum_original == checksum_compressed)

# Measure execution time for decompression
start_time = time.time()

# Decompress and load the data
with gzip.open('encoded_data.npy.gz', 'rb') as f_in:
    loaded_data = np.load(f_in)

decompression_time = time.time() - start_time  # Decompression time

# Calculate checksum of the decompressed data
checksum_decompressed = hashlib.md5(loaded_data).hexdigest()

# Verify data integrity after decompression
data_integrity_verified_decompression = (checksum_original == checksum_decompressed)

# Print results
print("Original size:", original_size, "bytes")
print("Compressed size:", len(compressed_data), "bytes")
print("Compression ratio:", original_size / len(compressed_data))
print("Compression time:", compression_time, "seconds")
print("Decompression time:", decompression_time, "seconds")
print("Data integrity verified after compression:", data_integrity_verified_compression)
print("Data integrity verified after decompression:", data_integrity_verified_decompression)

if not data_integrity_verified_compression or not data_integrity_verified_decompression:
    print("Warning: Data integrity check failed. The compressed data may be corrupted.")
else:
    print("Data has been compressed, saved, and loaded successfully.")
