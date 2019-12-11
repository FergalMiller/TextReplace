import os
import re
from typing import Dict, List

from abstract.RunProfile import RunProfile
from run_profiles.argument.Argument import Argument, ArgumentError


class FileLineByLineReWriter:
    @staticmethod
    def rewrite(target_file_path: str, schema: Dict[str, str]):
        with open(target_file_path, "r") as target_file:
            lines = target_file.readlines()
            index = 0
            for line in lines:
                for illegal_character in schema.keys():
                    line = line.replace(illegal_character, schema[illegal_character])
                lines[index] = line.__str__()
                index += 1

        with open(target_file_path, "w") as target_file:
            target_file.writelines(lines)


# Bulk file rewrite profile
class BulkFileRewriteRunProfile(RunProfile):
    arguments: List[Argument] = [
        Argument("-d", "The directory to traverse.", True),
        Argument("-e", "The file extension to search for.", False),
        Argument("-r", "The regex pattern to match file names.", False)
    ]

    def __init__(self, supplied_arguments: str):
        super().__init__(supplied_arguments)

    def filter_target_files(self, target_files: List[str]) -> List[str]:
        filter_extensions = self.get_argument_value("-e") != ""
        filter_by_regex_pattern = self.get_argument_value("-r") != ""

        file_path_pattern = r'([/[\w,-\.]+]*/)*([\w,-]+)\.+([A-Za-z]+)$'
        result: List[str] = []

        if filter_extensions or filter_by_regex_pattern:
            for target_file in target_files:
                if re.search(file_path_pattern, target_file):
                    matcher = re.match(file_path_pattern, target_file)
                    directory = matcher.group(1)
                    file_name = matcher.group(2)
                    extension = matcher.group(3)
                    # TODO: Employ helper methods to filter list to result list
        return result

    def run(self, schema: Dict[str, str]):
        # TODO: Manage update to Argument class now that arguments are instance variables in a profile.
        root_search_directory = self.get_argument_value("-d")
        target_files = []
        for root, dirs, files in os.walk(root_search_directory):
            for file in files:
                target_files.append(os.path.join(root, file))

        print("Checked files: ", target_files)

        # TODO: Filter list by extension and regex, then rewrite each file.

    @staticmethod
    def command() -> str: return "-b"

    def get_arguments(self) -> List[Argument]: return self.arguments


# Single file re-write profile
class SingleFileRewriteRunProfile(RunProfile):
    arguments: List[Argument] = [Argument("-p", "The file path.", True)]

    def __init__(self, supplied_arguments: str):
        super().__init__(supplied_arguments)

    def run(self, schema: Dict[str, str]):

        target_file_path = self.get_argument_value("-p")

        print('\033[92m' + "Replacing illegal characters in `" + target_file_path + "`" + '\033[0m')

        FileLineByLineReWriter.rewrite(target_file_path, schema)

    @staticmethod
    def command() -> str: return "-s"

    def get_arguments(self) -> List[Argument]: return self.arguments
