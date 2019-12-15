from typing import Pattern
from file_rewrite_profiles.regex_replacer.RegexRewriteCommand import RegexReWriteCommand


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
            # TODO: Rewrite file with result


'''re_writer = RegexFileReWriter(re.compile('(/\\*\\*)\\s*\\n\\s*\\*(.*)\\n\\s*(\\*/)'),
                              RegexReWriteCommand(0, ['1', '2', '{0}', '3'], [". "]))
re_writer.rewrite_file("../test.txt")'''
