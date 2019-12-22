import re
from typing import List, Pattern

from common.profile.abstract.FileRewriteProfile import FileRewriteProfile
from common.profile.argument.Argument import Argument
from common.profile.file_rewrite_profiles.regex_replacer.RegexFileReWriter import RegexFileReWriter
from common.profile.file_rewrite_profiles.regex_replacer.RegexRewriteCommand import RegexRewriteCommand


class RegexReplacerRewriteProfile(FileRewriteProfile):
    arguments = [
        Argument("-p", "The regex pattern to match", True, ""),
        Argument("-c", "The pattern replacement command.", True,
                 r'([0-9]+)\((([0-9]+|{[0-9]+})(,([0-9]+|{[0-9]+}))*)\)'),
        Argument("-param", "Argument for the replacement command", False, r'\"(((\\\')|[^\'])+)\"')
    ]
    supplied_argument_pattern: Pattern[str] = re.compile(r'(-\w+)\s?(\'(((\\\')|[^\'])+)\'|[^\s]+)')
    param_input_pattern: Pattern[str] = re.compile(r'\'(((\\\')|[^\'])+)\'')

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

    def parse_param(self, value: str) -> str:
        search = self.param_input_pattern.search(value)
        if search:
            value = search.group(1)
            value.replace("\\\'", "\'")
        else:
            raise Exception("Parameter " + value + " could not be understood. Please ensure it is formatted correctly.")
        return value

    def supply_argument_value(self, key: str, value: str):
        if key == "-param":
            value = self.parse_param(value)
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

    def parse_supplied_arguments(self, supplied_arguments: str):
        arg_list: List[str] = []

        arg_found = self.supplied_argument_pattern.search(supplied_arguments)
        while arg_found:
            full_match = arg_found.group(0)
            arg_list.append(full_match)
            supplied_arguments = supplied_arguments.replace(full_match, "")
            arg_found = self.supplied_argument_pattern.search(supplied_arguments)

        for arg in arg_list:
            arg = arg.strip()
            if not arg == "":
                try:
                    search = self.supplied_argument_pattern.search(arg)
                    key = search.group(1)
                    value = search.group(2)
                    self.supply_argument_value(key, value)
                except AttributeError:
                    print("Could not understand argument: ", arg)
