from abc import ABC, abstractmethod
from typing import Set, Dict


class SchemaGenerator(ABC):
    @staticmethod
    @abstractmethod
    def generate_schema(illegal_characters: Set[str]) -> Dict[str, str]: pass

    @staticmethod
    @abstractmethod
    def name() -> str: pass

    @staticmethod
    @abstractmethod
    def description() -> str: pass
