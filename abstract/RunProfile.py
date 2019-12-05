from abc import ABC, abstractmethod
from typing import Dict, List
from run_profiles.argument.Argument import Argument


class RunProfile(ABC):
    @abstractmethod
    def run(self, schema: Dict[str, str], arguments: Dict[str, str]): pass

    @abstractmethod
    def get_arguments(self) -> List[Argument]: pass

    @staticmethod
    @abstractmethod
    def command() -> str: pass
