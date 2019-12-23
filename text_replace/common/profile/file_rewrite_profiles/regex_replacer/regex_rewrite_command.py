import re
from typing import List, Pattern, Tuple, Match

from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_util.regex_util import GroupMatch, RegexUtil


class RegexRewriteCommand(object):
    group_to_replace: int
    replace_with: List[str]
    arguments = List[str]
    argument_pattern = re.compile(r'^{([0-9]+)}$')

    def validate_command_arguments(self):
        num_of_available_argument_indices = len(self.arguments) - 1
        for replacement_key in self.replace_with:
            search = self.argument_pattern.search(replacement_key)
            if search and int(search.group(1)) > num_of_available_argument_indices:
                raise Exception("Rewrite command cannot be validated: " + replacement_key +
                                " references an argument index higher than number of arguments supplied.")

    def __init__(self, group_to_replace: int, replace_with: List[str], arguments: List[str]):
        self.group_to_replace = group_to_replace
        self.replace_with = replace_with
        self.arguments = arguments
        self.validate_command_arguments()

    def get_replacement(self, full_match: str, pattern: Pattern[str]) -> str:
        group_match: GroupMatch = RegexUtil.get_group_match(full_match, pattern)
        result = ""
        for replacement in self.replace_with:
            search = self.argument_pattern.search(replacement)
            if search:
                replacement_argument_index = int(search.group(1))
                result += self.arguments[replacement_argument_index]
            else:
                replacement_group_index = int(replacement)
                if replacement_group_index == 0:
                    result += full_match
                else:
                    result += group_match.get_value_of_group(int(replacement))
        return result
