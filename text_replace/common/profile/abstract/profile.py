import re
from abc import ABC, abstractmethod
from typing import List

from text_replace.common.profile.argument.argument import Argument, ArgumentError


class Profile(ABC):
    """
    Profile is an abstract runnable class that can be supplied arguments to alter its behaviour.
    """
    @abstractmethod
    def get_arguments(self) -> List[Argument]:
        pass

    @staticmethod
    @abstractmethod
    def command() -> str: pass

    @staticmethod
    @abstractmethod
    def description() -> str: pass

    @abstractmethod
    def __init__(self, arguments: str):
        self.parse_supplied_arguments(arguments)
        self.validate_arguments()

    def get_argument(self, key: str) -> Argument:
        for argument in self.get_arguments():
            if argument.key == key:
                return argument
        raise ArgumentError("Could not find argument with key " + key + ".")

    def get_argument_value(self, key: str) -> str:
        return self.get_argument(key).value

    def supply_argument_value(self, key: str, value: str):
        for argument in self.get_arguments():
            if argument.key == key:
                argument.value = value
                return
        raise ArgumentError("Could not associate value " + value + ". No argument prefix found for " + key + ".")

    def parse_supplied_arguments(self, supplied_arguments: str):
        argument_pattern = re.compile(r'(-\w+\s?[^\s]+)')
        supplied_arguments: List[str] = argument_pattern.split(supplied_arguments)
        for supplied_argument in supplied_arguments:
            supplied_argument = supplied_argument.strip()
            if not supplied_argument == "":
                try:
                    argument_matcher = re.match(r'(-\w+)\s?([^\s]+)', supplied_argument)
                    key = argument_matcher.group(1)
                    value = argument_matcher.group(2)
                    self.supply_argument_value(key, value)
                except AttributeError:
                    print("Could not understand argument: ", supplied_argument)

    def validate_arguments(self):
        error_found = False
        for argument in self.get_arguments():
            try:
                argument.self_validate()
            except ArgumentError as e:
                error_found = True
                print('\033[91m' + "Argument error: " + e.reason + '\033[0m')
        if error_found:
            print("Exiting...")
            exit(1)
