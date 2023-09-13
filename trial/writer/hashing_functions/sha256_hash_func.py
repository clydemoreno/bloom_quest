from hashlib import sha256
import sys
from pathlib import Path

# Get the parent directory of the current script (where the hash function module is located)
module_dir = Path(__file__).resolve().parent

# Add the parent directory to sys.path
sys.path.append(str(module_dir))


# Get the parent directory of the current script (where the hash function module is located)
module_dir = Path(__file__).resolve().parent
# Add the parent directory to sys.path
sys.path.append(str(module_dir))

from IHashFunction import IHashFunction

class SHA256Hash(IHashFunction):

    def hash(self, input_str: str) -> int:
        hash_object = sha256(input_str.encode())
        hex_digest = hash_object.hexdigest()
        return int(hex_digest, 16)
