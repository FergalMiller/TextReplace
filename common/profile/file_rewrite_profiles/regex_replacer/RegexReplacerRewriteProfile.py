import re
from typing import List, Pattern

from common.profile.abstract.FileRewriteProfile import FileRewriteProfile
from common.profile.argument.Argument import Argument
from common.profile.file_rewrite_profiles.regex_replacer.RegexFileReWriter import RegexFileReWriter
from common.profile.file_rewrite_profiles.regex_replacer.RegexRewriteCommand import RegexRewriteCommand


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
            compiled_command: RegexRewriteCommand = self.generate_rewrite_command(string_rewrite_command)
            self.compiled_rewrite_commands.append(compiled_command)

        re_writer = RegexFileReWriter(pattern, self.compiled_rewrite_commands)
        re_writer.rewrite_file(target_file_path)

    def get_arguments(self) -> List[Argument]: return self.arguments

    @staticmethod
    def command() -> str: return "-rr"

    def generate_rewrite_command(self, command_as_string: str) -> RegexRewriteCommand:
        search = self.command_pattern.search(command_as_string)
        replacement_group = int(search.group(1))
        replace_with: List[str] = search.group(2).split(",")
        return RegexRewriteCommand(replacement_group, replace_with, self.arg_list)

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
