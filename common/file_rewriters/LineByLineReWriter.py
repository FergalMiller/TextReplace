from typing import Dict


class LineByLineReWriter(object):
    """"
    LineByLineReWriter is a simple file re-writing tool.
    It takes a target file path (as string) and a schema (as dictionary)
    and replaces matching schema keys in each line, line by line.
    """
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
