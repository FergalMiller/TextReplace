import os
import re
from typing import Dict, List

from abstract.RunProfile import RunProfile
from run_profiles.argument.Argument import Argument


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
        Argument("-d", "The directory to traverse.", True, r'^/?([\w\-\.]+/)+$'),
        Argument("-e", "The file extension to search for.", False, r'^\.?[a-z][a-zA-Z]*$'),
        Argument("-r", "The regex pattern to match file names.", False, "")
    ]

    def __init__(self, supplied_arguments: str):
        super().__init__(supplied_arguments)

    def verify_file_against_filters(self, directory: str, file_name: str, extension: str) -> bool:
        # Counts as matching if no value is required
        matches_extension_filter = self.get_argument_value("-e") == ""
        matches_pattern_filter =  self.get_argument_value("-r") == ""

        # Any non-matching filters are verified
        if not matches_extension_filter and extension.__eq__(self.get_argument_value("-e")):
            matches_extension_filter = True
        if not matches_pattern_filter:
            custom_pattern = self.get_argument_value("-r")
            if re.search(custom_pattern, file_name):
                matches_pattern_filter = True

        # File is verified if all filter matches true
        return matches_extension_filter and matches_pattern_filter

    def filter_target_files(self, target_files: List[str]) -> List[str]:
        filter_extensions = self.get_argument_value("-e") != ""
        filter_by_regex_pattern = self.get_argument_value("-r") != ""

        file_path_pattern = r'^(/?([\w\-\.]+/)+)*([\w\-\.]+)\.([a-z][a-zA-Z]*)$'
        result: List[str] = []

        if filter_extensions or filter_by_regex_pattern:
            for target_file in target_files:
                if re.search(file_path_pattern, target_file):
                    matcher = re.match(file_path_pattern, target_file)
                    directory = matcher.group(1)
                    file_name = matcher.group(3)
                    extension = matcher.group(4)
                    if self.verify_file_against_filters(directory, file_name, extension):
                        result.append(target_file)
        return result

    def run(self, schema: Dict[str, str]):
        root_search_directory = self.get_argument_value("-d")
        target_files = []
        for root, dirs, files in os.walk(root_search_directory):
            for file in files:
                target_files.append(os.path.join(root, file))

        target_files = self.filter_target_files(target_files)

        print('\033[92m' + "Identified target files for re-write: ")
        for target_file in target_files:
            print(target_file)
        print('\033[0m')

        while True:
            user_inp = input("Are you sure you want to carry out re-write on all files listed (y/n)? ")
            if user_inp == "y":
                for target_file in target_files:
                    print('\033[92m' + "Replacing illegal characters in `" + target_file + "`" + '\033[0m')
                    FileLineByLineReWriter.rewrite(target_file, schema)
                break
            elif user_inp == "n":
                print("Exiting without rewriting...")
                break
            else:
                print("Unrecognised input. Please write 'y' for yes, 'n' for no.")

    @staticmethod
    def command() -> str: return "-b"

    def get_arguments(self) -> List[Argument]: return self.arguments


# Single file re-write profile
class SingleFileRewriteRunProfile(RunProfile):
    arguments: List[Argument] = [Argument("-p",
                                          "The file path.",
                                          True,
                                          r'^(/?([\w\-\.]+/)+)*([\w\-\.]+)\.([a-z][a-zA-Z]*)$')]

    def __init__(self, supplied_arguments: str):
        super().__init__(supplied_arguments)

    def run(self, schema: Dict[str, str]):

        target_file_path = self.get_argument_value("-p")

        print('\033[92m' + "Replacing illegal characters in `" + target_file_path + "`" + '\033[0m')

        FileLineByLineReWriter.rewrite(target_file_path, schema)

    @staticmethod
    def command() -> str: return "-s"

    def get_arguments(self) -> List[Argument]: return self.arguments
