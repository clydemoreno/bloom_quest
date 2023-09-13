from pathlib import Path
import sys
# Get the parent directory of the current script (where the hash function module is located)
module_dir = Path(__file__).resolve().parent
# Add the parent directory to sys.path
sys.path.append(str(module_dir))

from IHashFunction import IHashFunction

class SuperFastHash(IHashFunction):

    def hash(self, input_str: str) -> int:
        hash_value = 0
        length = 0

        for byte in input_str.encode('utf-8'):
            hash_value = (hash_value << 5) ^ byte
            length += 1

        # Perform a final XOR with the length
        hash_value ^= length

        return hash_value
