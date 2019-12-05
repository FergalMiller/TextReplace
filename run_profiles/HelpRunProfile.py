from abstract.RunProfile import RunProfile
from run_profiles.argument.Argument import Argument
from typing import Dict, List


class HelpRunProfile(RunProfile):
    arguments = []

    def run(self, schema: Dict[str, str], arguments: Dict[str, str]):
        # TODO
        print(self.arguments)

    @staticmethod
    def command() -> str: return "-h"

    def get_arguments(self) -> List[Argument]: return self.arguments
