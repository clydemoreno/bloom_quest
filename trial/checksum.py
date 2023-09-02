import unittest

def checksum(bitarray: list):
    chunk_size = 32
    array_size = len(bitarray)
    #seed is zero
    checksum = [0] * chunk_size
    #edge case
    if len(bitarray) == 0:
        return checksum
    
    for i in range(0, len(bitarray), chunk_size):
        chunk = bitarray[i: i + chunk_size]
        if len(chunk) < chunk_size:
            chunk.extend([0] * (chunk_size - len(chunk)))

        for j in range(len(chunk)):
            checksum[j] ^= chunk[j]

        print(f"i:{i}, checksum: `{checksum}`")
    
    return checksum

# Implementations
def calculate_32bit_xor_checksum(data):
    chunk_size = 32
    checksum = [0] * 32  # Initialize a 32-bit checksum as a bit array
    
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        if len(chunk) < chunk_size:
            chunk.extend([0] * (chunk_size - len(chunk)))  # Pad with zeroes
        chunk_checksum = [bit for bit in chunk]  # Initialize chunk_checksum with chunk bits
        for _ in range(chunk_size - len(chunk)):
            chunk_checksum.append(0)  # Pad chunk_checksum with zeroes
        
        # XOR the chunk_checksum with the current checksum
        for j in range(32):
            checksum[j] ^= chunk_checksum[j]
    # print ("checksum",checksum)
    return checksum

def verify_32bit_xor_checksum(data, checksum):
    calculated_checksum = calculate_32bit_xor_checksum(data)
    return calculated_checksum == checksum

# Test data
class Test32BitXORChecksum(unittest.TestCase):
    def test_empty_bitarray(self):
        result = calculate_32bit_xor_checksum([])
        expected = [0] * 32
        self.assertEqual(result, expected)

    def test_single_chunk_bitarray(self):
        result = calculate_32bit_xor_checksum([1, 0, 1])
        result = checksum([1, 0, 1])
        expected = [0, 1, 0] + ([0] * 29)
        # self.assertEqual(result, expected)

    def test_32bit_bitarray(self):
        bitarray = [1] * 32
        result = calculate_32bit_xor_checksum(bitarray)
        expected = [1] * 32
        self.assertEqual(result, expected)


        bitarray = [0] * 32
        result = calculate_32bit_xor_checksum(bitarray)
        expected = [0] * 32
        self.assertEqual(result, expected)


    def test_64bit_bitarray(self):
        bitarray = [1] * 64
        result = calculate_32bit_xor_checksum(bitarray)
        expected = [0] * 32 
        self.assertEqual(result, expected)

        bitarray = [0] * 64
        result = calculate_32bit_xor_checksum(bitarray)
        expected = [0] * 32 
        self.assertEqual(result, expected)


    def test_96bit_bitarray(self):
        bitarray = [1] * 96
        result = calculate_32bit_xor_checksum(bitarray)
        expected = [1] * 32 
        self.assertEqual(result, expected)

        bitarray = [0] * 96
        result = calculate_32bit_xor_checksum(bitarray)
        expected = [0] * 32 
        self.assertEqual(result, expected)

    def test_128bit_bitarray(self):
        bitarray = [1] * 128
        result = calculate_32bit_xor_checksum(bitarray)
        expected = [0] * 32 
        self.assertEqual(result, expected)

        bitarray = [0] * 128
        result = calculate_32bit_xor_checksum(bitarray)
        expected = [0] * 32 
        self.assertEqual(result, expected)

    def test_mixture_35_and_97(self):
        bitarray = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        result = calculate_32bit_xor_checksum(bitarray)
        expected = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        self.assertEqual(result, expected)

        bitarray = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        result = calculate_32bit_xor_checksum(bitarray)
        expected = [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        self.assertNotEqual(result, expected)


    def fletcher16(data):
        sum1 = 0
        sum2 = 0

        for byte in data:
            sum1 = (sum1 + byte) % 255
            sum2 = (sum2 + sum1) % 255

        checksum = (sum2 << 8) | sum1
        return checksum

    # Example usage
    input_string = "Hello, world!"
    ascii_values = [ord(char) for char in input_string]
    checksum = fletcher16(ascii_values)
    print(f"Fletcher's checksum: {hex(checksum)}")


if __name__ == '__main__':
    # Define the string you want to write to the file
    content = "Hello, this is some text that will be written to a file."

    # Specify the file path
    file_path = "./output.txt"

    # Open the file in write mode and write the content
    with open(file_path, "w") as file:
        file.write(content)

    # print(f"String has been written to {file_path}")    
    # unittest.main()
    # bitarray = [1] * 64
    # # result = calculate_32bit_xor_checksum(bitarray)
    # result = checksum(bitarray)

    # # # print("result",len(result))

    # expected = [0] * 32 
    # # print (expected)
    # # print (result)


        # arr2 = [0] * 5
    # chunk_size = 32
        
    # print(checksum(arr))
    # print(calculate_32bit_xor_checksum(arr))

    # arr = [0, 1,0]
    # assert(checksum(arr) == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    # arr = [1, 0,1]
    # assert(checksum(arr) == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

