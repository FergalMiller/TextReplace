from abc import ABC, abstractmethod


class SchemaGenerator(ABC):
    @staticmethod
    @abstractmethod
    def generate_schema(illegal_characters: list) -> dict: pass

    @staticmethod
    @abstractmethod
    def name() -> str: pass

    @staticmethod
    @abstractmethod
    def description() -> str: pass
