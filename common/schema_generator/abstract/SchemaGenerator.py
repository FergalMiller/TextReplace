from abc import ABC, abstractmethod
from typing import Set, Dict


class SchemaGenerator(ABC):
    """
    SchemaGenerator is an abstract class that generates simple dictionary type schemas.
    Given a set of strings it will create a corresponding key/value pair in the schema.
    """
    @staticmethod
    @abstractmethod
    def generate_schema(illegal_characters: Set[str]) -> Dict[str, str]: pass
