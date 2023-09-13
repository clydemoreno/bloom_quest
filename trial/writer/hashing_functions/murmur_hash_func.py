from pathlib import Path
import sys
# Get the parent directory of the current script (where the hash function module is located)
module_dir = Path(__file__).resolve().parent
# Add the parent directory to sys.path
sys.path.append(str(module_dir))

from IHashFunction import IHashFunction

class MurmurHash(IHashFunction):

    def hash(self, input_str):
        m = 0x5bd1e995
        seed = 0
        length = len(input_str)

        def mix(h, k):
            k *= m
            k ^= k >> 24
            k *= m
            h *= m
            h ^= k

            return h

        hash_value = seed ^ length

        index = 0

        while length >= 4:
            chunk = (
                (ord(input_str[index + 3]) << 24) |
                (ord(input_str[index + 2]) << 16) |
                (ord(input_str[index + 1]) << 8) |
                ord(input_str[index])
            )

            chunk = mix(chunk, m)
            hash_value = mix(hash_value, chunk)

            index += 4
            length -= 4

        tail = 0

        for shift in range(0, length * 8, 8):
            tail ^= (ord(input_str[index]) << shift)
            index += 1

        tail = mix(tail, m)
        hash_value ^= tail

        hash_value ^= hash_value >> 13
        hash_value *= m
        hash_value ^= hash_value >> 15

        return hash_value & 0xFFFFFFFF
