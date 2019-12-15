import re

from typing import List, Pattern


# ([0-9]+)\((([0-9]+|{[0-9]+})(,([0-9]+|{[0-9]+}))*)\) command regex
class RegexReWriteCommand(object):
    group_to_replace: int
    replace_with: List[str]
    arguments = List[str]
    argument_pattern = re.compile(r'^{([0-9]+)}$')

    def __init__(self, group_to_replace: int, replace_with: List[str], arguments: List[str]):
        self.group_to_replace = group_to_replace
        self.replace_with = replace_with
        self.arguments = arguments

    def get_replacement(self, full_match: str, pattern: Pattern[str]) -> str:
        groups = pattern.split(full_match)
        result = ""
        for replacement in self.replace_with:
            search = self.argument_pattern.search(replacement)
            if search:
                result += self.arguments[int(search.group(1))]
            else:
                group_to_replace = groups[int(replacement)]
                if group_to_replace == 0:
                    result += full_match
                else:
                    result += groups[int(replacement)]
        return result


class RegexReWriteCommandBuilder(object):
    group_to_replace: int
    replace_with: List[str]
    arguments = List[str]
    num_of_arguments: int

    def __init__(self, group_to_replace: int):
        self.group_to_replace = group_to_replace
        self.num_of_arguments = 0

    def add_argument(self, argument: str):
        self.arguments.append(argument)
        return self

    def set_replace_with(self, replace_with: List[str]):
        self.replace_with = replace_with
        return self

    def build(self) -> RegexReWriteCommand:
        return RegexReWriteCommand(self.group_to_replace, self.replace_with, self.arguments)


# TODO: Validate that write command does not have out of bound groups
class RegexFileReWriter(object):
    pattern: Pattern[str]
    rewrite_command: RegexReWriteCommand

    def __init__(self, pattern: Pattern[str], rewrite_command: RegexReWriteCommand):
        self.pattern = pattern
        self.rewrite_command = rewrite_command

    def modify_match(self, full_match: str) -> str:
        match_split = self.pattern.split(full_match)

        to_replace: str
        if self.rewrite_command.group_to_replace == 0:
            to_replace = full_match
        else:
            to_replace = match_split[self.rewrite_command.group_to_replace]

        replace_with = self.rewrite_command.get_replacement(full_match, self.pattern)

        return full_match.replace(to_replace, replace_with)

    def recursive_match_result(self, to_match: str) -> str:
        search = self.pattern.search(to_match)
        if search:
            full_match = self.pattern.search(to_match).group(0)
            no_of_groups = self.pattern.groups
            match_split = self.pattern.split(to_match, 1)
            modified_match = "(" + self.modify_match(full_match) + ")"
            return \
                match_split[0] + \
                modified_match + \
                RegexFileReWriter.recursive_match_result(self, match_split[no_of_groups + 1])
        return to_match

    def rewrite_file(self, target_file_path: str):
        with open(target_file_path) as target_file:
            to_match = target_file.read()
            result = self.recursive_match_result(to_match)
            print(result)


re_writer = RegexFileReWriter(re.compile('(/\\*\\*)\\s*\\n\\s*\\*(.*)\\n\\s*(\\*/)'),
                              RegexReWriteCommand(0, ['1', '2', '{0}', '3'], [". "]))
re_writer.rewrite_file("../test.txt")
