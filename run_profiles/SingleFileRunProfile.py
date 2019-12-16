from typing import List

from abstract.FileRewriteProfile import FileRewriteProfile
from abstract.RunProfile import RunProfile
from common.argument.Argument import Argument


class SingleFileRunProfile(RunProfile):
    arguments: List[Argument] = [Argument("-p", "The file path.", True,
                                          r'^(/?([\w\-\.]+/)+)*([\w\-\.]+)\.([a-z][a-zA-Z]*)$')]

    def __init__(self, rewrite_profile_arguments: str):
        super().__init__(rewrite_profile_arguments)

    def run(self, file_rewrite_profile: FileRewriteProfile):

        target_file_path = self.get_argument_value("-p")

        print('\033[92m' + "Replacing text in `" + target_file_path + "`" + '\033[0m')

        file_rewrite_profile.run(target_file_path)

    @staticmethod
    def command() -> str: return "-s"

    def get_arguments(self) -> List[Argument]: return self.arguments
