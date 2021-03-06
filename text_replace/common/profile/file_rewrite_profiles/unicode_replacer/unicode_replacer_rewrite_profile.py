from typing import List, Set

from text_replace.common.profile.abstract.file_rewrite_profile import FileRewriteProfile
from text_replace.common.profile.argument.argument import Argument
from text_replace.common.file_rewriters.line_by_line_rewriter import LineByLineRewriter
from text_replace.common.profile.file_rewrite_profiles.unicode_replacer.unicode_escape_schema_generator import UnicodeSchemaGenerator


class UnicodeReplacerRewriteProfile(FileRewriteProfile):
    arguments: List[Argument]

    @staticmethod
    def get_illegal_characters(illegal_characters_location) -> Set[str]:
        illegal_characters = set()
        try:
            with open(illegal_characters_location) as illegal_characters_file:
                content = illegal_characters_file.read().strip()
                for c in list(content):
                    if not (c == ' ' or c == '\n'):
                        illegal_characters.add(c)
        except FileNotFoundError:
            print("Error! Illegal character file not present under path '", illegal_characters_location + "'")
            illegal_characters = UnicodeReplacerRewriteProfile\
                .get_illegal_characters(input("Enter the path of your illegal characters text file:"))
        return illegal_characters

    def run(self, target_file_path):
        illegal_character_location = self.get_argument("-i").value
        illegal_characters = UnicodeReplacerRewriteProfile.get_illegal_characters(illegal_character_location)
        schema = UnicodeSchemaGenerator.generate_schema(illegal_characters)
        LineByLineRewriter.rewrite(target_file_path, schema)

    def get_arguments(self) -> List[Argument]: return self.arguments

    @staticmethod
    def command() -> str: return "-uc"

    @staticmethod
    def description() -> str: return "Rewrites all matching illegal characters to their escaped unicode counterpart."

    @staticmethod
    def get_static_arguments() -> List[Argument]:
        return [Argument("-i",
                         "Location of the illegal characters file",
                         True,
                         r'^(/?([\w\-\.]+/)+)*([\w\-\.]+)\.([a-z][a-zA-Z]*)$')]

    def __init__(self, arguments: str): super().__init__(arguments)
