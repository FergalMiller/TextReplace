import re
from typing import List, Pattern

from abstract.FileRewriteProfile import FileRewriteProfile
from common.argument.Argument import Argument


# comment = r'(/\*\s*\n\s*\*(.*)\n\s*\*\*/)'
from file_rewrite_profiles.regex_replacer import RegexRewriteCommand
from file_rewrite_profiles.regex_replacer.RegexFileReWriter import RegexFileReWriter


class RegexReplacerRewriteProfile(FileRewriteProfile):
    arguments = [
        Argument("-p", "The regex pattern to match", True, ""),
        Argument("-c", "The pattern replacement command.", True,
                 r'([0-9]+)\((([0-9]+|{[0-9]+})(,([0-9]+|{[0-9]+}))*)\)'),
        Argument("-arg", "Argument for the replacement command", False, "")

    ]

    def __init__(self, rewrite_profile_arguments: str):
        super().__init__(rewrite_profile_arguments)

    def run(self, target_file_path):
        pattern_as_string: str = self.get_argument_value("p")
        pattern: Pattern[str] = re.compile(pattern_as_string)

        # TODO:
        #  Find a way to pass multiple arguments to the arg parameter.
        #  Generate regex rewrite command.
        #  Run re-writer.

    def get_arguments(self) -> List[Argument]: return self.arguments

    @staticmethod
    def command() -> str: return "-rr"
