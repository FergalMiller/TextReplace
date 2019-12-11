from abstract.RunProfile import RunProfile
from run_profiles.argument.Argument import Argument
from typing import Dict, List


class HelpRunProfile(RunProfile):

    def run(self, schema: Dict[str, str]):
        # TODO
        print("TODO")

    def __init__(self, supplied_arguments: str):
        super().__init__(supplied_arguments)

    def parse_supplied_arguments(self, supplied_arguments: str): pass

    def validate_arguments(self): pass

    @staticmethod
    def command() -> str: return "-h"

    def get_arguments(self) -> List[Argument]: return []
