

# ([0-9]+)\((([0-9]+|{[0-9]+})(,([0-9]+|{[0-9]+}))*)\) command regex
import re
from typing import List, Pattern


class RegexRewriteCommand(object):
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


class RegexRewriteCommandBuilder(object):
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

    def build(self) -> RegexRewriteCommand:
        return RegexRewriteCommand(self.group_to_replace, self.replace_with, self.arguments)
