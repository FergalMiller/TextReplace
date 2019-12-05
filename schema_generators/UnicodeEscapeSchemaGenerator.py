import os
import re

from abstract.SchemaGenerator import SchemaGenerator


class UnicodeSchemaGenerator(SchemaGenerator):

    @staticmethod
    def generate_schema(illegal_characters: list) -> dict:
        schema = {}
        escape_pattern = r'\\u[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]'

        with open('temp.txt', 'w') as inp_file:
            for c in illegal_characters:
                inp_file.write(c + ",")

        os.system("native2ascii -encoding utf8 temp.txt temp.txt")

        with open('temp.txt', 'r') as out_file:
            escaped_characters = out_file.read().split(',')

        os.remove("temp.txt")

        index = 0
        for character in illegal_characters:
            escaped_character = escaped_characters[index]
            if re.compile(escape_pattern).search(escaped_character):
                schema[character] = escaped_character
            else:
                print('\033[91m' + "WARNING: character `" + character +
                      "` cannot be escaped. Not added to schema." + '\033[0m')
            index += 1

        return schema

    @staticmethod
    def name() -> str: return "Unicode escape schema generator"

    @staticmethod
    def description() -> str: return "Matches non-standard characters to their unicode escaped counterpart."
