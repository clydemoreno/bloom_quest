import abc
import mmh3

from IHashFunction import IHashFunction


class MurmurHash3(IHashFunction):
    def hash(self, input_str: str) -> int:
        return mmh3.hash(input_str)

# Example usage:
if __name__ == "__main__":
    hash_function = MurmurHash3()
    input_str = "Hello, World!"
    hash_value = hash_function.hash(input_str)
    print(f"Hash value for '{input_str}': {hash_value}")
