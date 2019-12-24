import re
from typing import List, Pattern

from text_replace.common.profile.abstract.file_rewrite_profile import FileRewriteProfile
from text_replace.common.profile.argument.argument import Argument
from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_file_rewriter import RegexFileRewriter
from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_rewrite_command import RegexRewriteCommand


# comment = r'(/\*\s*\n\s*\*(.*)\n\s*\*\*/)'
class RegexReplacerRewriteProfile(FileRewriteProfile):
    arguments = [
        Argument("-p", "The regex pattern to match", True, ""),
        Argument("-c", "The pattern replacement command.", True,
                 r'([0-9]+)\((([0-9]+|{[0-9]+})(,([0-9]+|{[0-9]+}))*)\)'),
        Argument("-param", "Argument for the replacement command", False, "")
    ]

    command_pattern = re.compile(r'^([0-9]+)\((([0-9]+|{[0-9]+})(,([0-9]+|{[0-9]+}))*)\)$')
    string_rewrite_commands: List[str] = []
    compiled_rewrite_commands: List[RegexRewriteCommand] = []
    arg_list: List[str] = []

    def __init__(self, rewrite_profile_arguments: str):
        super().__init__(rewrite_profile_arguments)

    def run(self, target_file_path):
        pattern_as_string: str = self.get_argument_value("-p")
        pattern: Pattern[str] = re.compile(pattern_as_string)

        for string_rewrite_command in self.string_rewrite_commands:
            compiled_command: RegexRewriteCommand = \
                RegexRewriteCommand.generate_rewrite_command(string_rewrite_command, self.arg_list)
            self.compiled_rewrite_commands.append(compiled_command)

        re_writer = RegexFileRewriter(pattern, self.compiled_rewrite_commands)
        re_writer.rewrite_file(target_file_path)

    def get_arguments(self) -> List[Argument]: return self.arguments

    @staticmethod
    def command() -> str: return "-rr"

    def supply_argument_value(self, key: str, value: str):
        if key == "-param":
            self.arg_list.append(value)
        elif key == "-c":
            if self.command_pattern.search(value):
                self.string_rewrite_commands.append(value)
                self.get_argument("-c").value = value
            else:
                # TODO: Handle
                raise Exception("Rewrite command not formatted correctly.")
        else:
            super().supply_argument_value(key, value)
