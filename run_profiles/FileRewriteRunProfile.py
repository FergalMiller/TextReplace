from abstract.RunProfile import RunProfile
from run_profiles.argument.Argument import Argument, ArgumentError
from typing import Dict, List


# Bulk file rewrite profile
class BulkFileRewriteRunProfile(RunProfile):
    arguments: List[Argument] = [
        Argument("-d", "The directory to traverse.", True),
        Argument("-e", "The file extension to search for.", False),
        Argument("-r", "The regex patter to match file names.", False)
    ]

    def run(self, schema: Dict[str, str], arguments: Dict[str, str]):
        # TODO
        print(self.arguments)

    @staticmethod
    def command() -> str: return "-b"

    def get_arguments(self) -> List[Argument]: return self.arguments


# Single file re-write profile
class SingleFileRewriteRunProfile(RunProfile):
    arguments: List[Argument] = [Argument("-path", "The file path.", True)]

    def run(self, schema: Dict[str, str], arguments: Dict[str, str]):
        try:
            self.validate_arguments(arguments)
        except ArgumentError as e:
            print("Argument error: " + e.reason)
            return

        target_file_path = arguments["-path"]
        print('\033[92m' + "Replacing illegal characters in `" + target_file_path + "`" + '\033[0m')

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

    @staticmethod
    def command() -> str: return "-s"

    def get_arguments(self) -> List[Argument]: return self.arguments
