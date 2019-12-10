from abc import ABC, abstractmethod
from typing import Dict, List
from run_profiles.argument.Argument import Argument, ArgumentError


class RunProfile(ABC):
    @abstractmethod
    def run(self, schema: Dict[str, str], arguments: Dict[str, str]): pass

    @abstractmethod
    def get_arguments(self) -> List[Argument]: pass

    @staticmethod
    @abstractmethod
    def command() -> str: pass

    def validate_arguments(self, supplied_arguments: Dict[str, str]) -> None:
        for argument in self.get_arguments():
            if argument.required:
                if not supplied_arguments.__contains__(argument.prefix):
                    raise ArgumentError("Required argument '" + argument.prefix +
                                        "' (" + argument.hint + ") to run with this profile")
