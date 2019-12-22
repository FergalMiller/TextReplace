from typing import Pattern, List
from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_rewrite_command import RegexRewriteCommand


# TODO: Validate that write command does not have out of bound groups
class RegexFileReWriter(object):
    pattern: Pattern[str]
    rewrite_commands: List[RegexRewriteCommand]

    def __init__(self, pattern: Pattern[str], rewrite_commands: List[RegexRewriteCommand]):
        self.pattern = pattern
        self.rewrite_commands = rewrite_commands

    def modify_match(self, full_match: str) -> str:
        result = full_match
        for rewrite_command in self.rewrite_commands:
            if self.pattern.search(result):
                match_split = self.pattern.split(full_match)
                to_replace: str
                if rewrite_command.group_to_replace == 0:
                    to_replace = full_match
                else:
                    to_replace = match_split[rewrite_command.group_to_replace]
                replace_with = rewrite_command.get_replacement(full_match, self.pattern)
                result = result.replace(to_replace, replace_with)
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
                RegexFileReWriter.recursive_match_result(self, match_split[no_of_groups + 1])
        return to_match

    def rewrite_file(self, target_file_path: str):
        result: str
        with open(target_file_path, 'r') as target_file:
            to_match = target_file.read()
            result = self.recursive_match_result(to_match)
        with open(target_file_path, 'w') as target_file:
            target_file.write(result)
