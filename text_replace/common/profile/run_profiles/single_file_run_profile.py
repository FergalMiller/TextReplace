from typing import List

from text_replace.common.profile.abstract.file_rewrite_profile import FileRewriteProfile
from text_replace.common.profile.abstract.run_profile import RunProfile
from text_replace.common.profile.argument.argument import Argument


class SingleFileRunProfile(RunProfile):
    arguments: List[Argument]

    def __init__(self, rewrite_profile_arguments: str):
        super().__init__(rewrite_profile_arguments)

    def run(self, file_rewrite_profile: FileRewriteProfile):

        target_file_path = self.get_argument_value("-p")

        print('\033[92m' + "Replacing text in `" + target_file_path + "`" + '\033[0m')

        file_rewrite_profile.run(target_file_path)

    @staticmethod
    def command() -> str: return "-s"

    @staticmethod
    def description() -> str: return "Runs a file rewrite profile on a single file."

    @staticmethod
    def get_static_arguments() -> List[Argument]:
        return [Argument("-p", "The file path.", True,r'^(/?([\w\-\.]+/)+)*([\w\-\.]+)\.([a-z][a-zA-Z]*)$')]

    def get_arguments(self) -> List[Argument]: return self.arguments
