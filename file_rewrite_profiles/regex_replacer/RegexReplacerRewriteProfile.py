from typing import List

from abstract.FileRewriteProfile import FileRewriteProfile
from common.argument.Argument import Argument


# comment = r'(/\*\s*\n\s*\*(.*)\n\s*\*\*/)'
class RegexReplacerRewriteProfile(FileRewriteProfile):
    arguments = [
        Argument("-p", "The regex pattern to match", True, ""),
        Argument("-g", "The groups to replace", True, r'([0-9]+)\(([0-9]+(,[0-9]+)*)\)')
    ]

    def __init__(self, rewrite_profile_arguments: str):
        super().__init__(rewrite_profile_arguments)

    def run(self, target_file_path):

        pass

    def get_arguments(self) -> List[Argument]: return self.arguments

    @staticmethod
    def command() -> str: return "-rr"
