from abc import ABC, abstractmethod


class SchemaGenerator(ABC):
    @staticmethod
    @abstractmethod
    def generate_schema(illegal_characters: list) -> dict:
        pass
