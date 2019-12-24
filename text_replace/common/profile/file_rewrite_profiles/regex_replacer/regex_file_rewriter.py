from typing import Pattern, List

from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_rewrite_command import RegexRewriteCommand
from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_util.regex_util import RegexUtil


# TODO: Validate that write command does not have out of bound groups
class RegexFileRewriter(object):
    pattern: Pattern[str]
    rewrite_commands: List[RegexRewriteCommand]

    def __init__(self, pattern: Pattern[str], rewrite_commands: List[RegexRewriteCommand]):
        self.pattern = pattern
        self.rewrite_commands = rewrite_commands

    def modify_match(self, full_match: str) -> str:
        result = full_match
        for rewrite_command in self.rewrite_commands:
            if self.pattern.search(result):
                group_to_replace = rewrite_command.group_to_replace

                group_match = RegexUtil.get_group_match(result, self.pattern)

                replacement_begin_index = group_match.get_begin_position_of_group(group_to_replace)
                replacement_end_index = group_match.get_end_position_of_group(group_to_replace)

                replace_with = rewrite_command.get_replacement(result, self.pattern)

                result = result[:replacement_begin_index] + replace_with + result[replacement_end_index:]
            else:
                break
        return result

    def recursive_match_result(self, to_match: str) -> str:
        search = self.pattern.search(to_match)
        if search:
            full_match = self.pattern.search(to_match).group(0)
            no_of_groups = self.pattern.groups
            match_split = self.pattern.split(to_match, 1)
            modified_match = self.modify_match(full_match)
            return \
                match_split[0] + \
                modified_match + \
                self.recursive_match_result(match_split[no_of_groups + 1])
        return to_match

    def rewrite_file(self, target_file_path: str):
        result: str
        with open(target_file_path, 'r') as target_file:
            to_match = target_file.read()
            result = self.recursive_match_result(to_match)
        with open(target_file_path, 'w') as target_file:
            target_file.write(result)
