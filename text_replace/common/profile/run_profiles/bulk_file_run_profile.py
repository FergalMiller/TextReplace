import os
import re
from typing import List

from text_replace.common.profile.abstract.file_rewrite_profile import FileRewriteProfile
from text_replace.common.profile.abstract.run_profile import RunProfile
from text_replace.common.profile.argument.argument import Argument


# Bulk file rewrite profile
class BulkFileRunProfile(RunProfile):
    arguments: List[Argument]

    def __init__(self, rewrite_profile_arguments: str):
        super().__init__(rewrite_profile_arguments)

    def verify_file_against_filters(self, directory: str, file_name: str, extension: str) -> bool:
        # Counts as matching if no value is required
        matches_extension_filter = self.get_argument_value("-e") == ""
        matches_pattern_filter = self.get_argument_value("-r") == ""

        # Any non-matching filters are verified
        if not matches_extension_filter and extension.__eq__(self.get_argument_value("-e")):
            matches_extension_filter = True
        if not matches_pattern_filter:
            custom_pattern = re.compile(self.get_argument_value("-r"))
            if custom_pattern.search(file_name):
                matches_pattern_filter = True

        # File is verified if all filter matches true
        return matches_extension_filter and matches_pattern_filter

    def filter_target_files(self, target_files: List[str]) -> List[str]:
        filter_extensions = self.get_argument_value("-e") != ""
        filter_by_regex_pattern = self.get_argument_value("-r") != ""

        file_path_pattern = re.compile(r'^(/?([\w\-.]+/)+)*([\w\-.]+)\.([a-z][a-zA-Z]*)$')
        result: List[str] = []

        if filter_extensions or filter_by_regex_pattern:
            for target_file in target_files:
                if file_path_pattern.search(target_file):
                    matcher = file_path_pattern.match(target_file)
                    directory = matcher.group(1)
                    file_name = matcher.group(3)
                    extension = matcher.group(4)
                    if self.verify_file_against_filters(directory, file_name, extension):
                        result.append(target_file)
        return result

    def run(self, file_rewrite_profile: FileRewriteProfile):
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
                    print('\033[92m' + "Replacing text in `" + target_file + "`" + '\033[0m')
                    file_rewrite_profile.run(target_file)
                break
            elif user_inp == "n":
                print("Exiting without rewriting...")
                break
            else:
                print("Unrecognised input. Please write 'y' for yes, 'n' for no.")

    @staticmethod
    def command() -> str: return "-b"

    @staticmethod
    def description() -> str: return "Runs a file rewrite profile on files in a given directory."

    @staticmethod
    def get_static_arguments() -> List[Argument]:
        return [
            Argument("-d", "The directory to traverse.", True, r'^/?([\w\-\.]+/)+$'),
            Argument("-e", "The file extension to search for.", False, r'^\.?[a-z][a-zA-Z]*$'),
            Argument("-r", "The regex pattern to match file names.", False, "")]

    def get_arguments(self) -> List[Argument]: return self.arguments
