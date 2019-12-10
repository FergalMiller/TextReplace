from abstract.RunProfile import RunProfile
from run_profiles.argument.Argument import Argument, ArgumentError
from typing import Dict, List


# Bulk file rewrite profile
class BulkFileRewriteRunProfile(RunProfile):
    arguments: List[Argument] = [
        Argument("-d", "The directory to traverse.", True),
        Argument("-e", "The file extension to search for.", False),
        Argument("-r", "The regex patter to match file names.", False)
    ]

    def run(self, schema: Dict[str, str], arguments: Dict[str, str]):
        # TODO
        print(self.arguments)

    @staticmethod
    def command() -> str: return "-b"

    def get_arguments(self) -> List[Argument]: return self.arguments


# Single file re-write profile
class SingleFileRewriteRunProfile(RunProfile):
    arguments: List[Argument] = [Argument("-path", "The file path.", True)]

    def run(self, schema: Dict[str, str], arguments: Dict[str, str]):
        # TODO
        print(self.arguments)

    @staticmethod
    def command() -> str: return "-s"

    def get_arguments(self) -> List[Argument]: return self.arguments
