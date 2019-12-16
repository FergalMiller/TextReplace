import os
import re
from typing import Dict, Set

from abstract.SchemaGenerator import SchemaGenerator


class UnicodeSchemaGenerator(SchemaGenerator):

    @staticmethod
    def generate_schema(illegal_characters: Set[str]) -> Dict[str, str]:
        schema = {}
        escape_pattern = r'\\u[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]'
        temp_file_name = "UNICODE____TEMP____FILE____.txt"

        with open(temp_file_name, 'w') as inp_file:
            for c in illegal_characters:
                inp_file.write(c + ",")

        os.system("native2ascii -encoding utf8 " + temp_file_name + " " + temp_file_name)

        with open(temp_file_name, 'r') as out_file:
            escaped_characters = out_file.read().split(',')

        os.remove(temp_file_name)

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
