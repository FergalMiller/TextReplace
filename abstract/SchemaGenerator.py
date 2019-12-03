from abc import ABC, abstractmethod


class SchemaGenerator(ABC):
    illegal_characters = []

    def __init__(self, illegal_characters):
        self.illegal_characters = illegal_characters

    @abstractmethod
    def generate_schema(self) -> dict:
        pass

