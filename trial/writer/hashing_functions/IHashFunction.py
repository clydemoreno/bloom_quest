import abc

class IHashFunction(abc.ABC):

    @abc.abstractmethod
    def hash(self, input_str: str) -> int:
        pass