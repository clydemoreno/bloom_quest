import cityhash
import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent
# Add the 'messaging' directory to sys.path
sys.path.append(str(parent_dir))

from IHashFunction import IHashFunction  # Import the IHashFunction class from the other module

class CityHash3pl(IHashFunction):
    def hash(self, input_str: str) -> int:
        return cityhash.CityHash64(input_str.encode('utf-8'))


if __name__ == "__main__":
    superfast_hash_function = CityHash3pl()

    input_str = "Hello, World!"

    superfast_hash_value = superfast_hash_function.hash(input_str)

    print(f"SuperfastHash value for '{input_str}': {superfast_hash_value}")
