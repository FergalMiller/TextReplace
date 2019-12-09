from typing import Dict, List, Set
from abstract.SchemaGenerator import SchemaGenerator
from abstract.RunProfile import RunProfile
from schema_generators.UnicodeEscapeSchemaGenerator import UnicodeSchemaGenerator
from run_profiles.HelpRunProfile import HelpRunProfile
from run_profiles.FileRewriteRunProfile import BulkFileRewriteRunProfile, SingleFileRewriteRunProfile
import sys


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
        illegal_characters = get_illegal_characters(input("Enter the path of your illegal characters text file:"))
    return illegal_characters


def get_user_input(upper_bound: int) -> int:
    while True:
        try:
            inp = int(input())
            if inp < 1 or inp > upper_bound:
                print("Not a valid index. Please try again.")
                return get_user_input(upper_bound)
            else:
                return inp
        except ValueError:
            print("Could not understand. Please try again.")
            return get_user_input(upper_bound)


def choose_schema_generator() -> SchemaGenerator:
    print('\033[95m' + "Please choose a schema generator" + '\033[0m')
    index = 0
    for schema_generator in schema_generators:
        print("Enter '" + (index + 1).__str__() + "' for " + schema_generator.name())
        print("\t" + schema_generator.description())
        index += 1
    return schema_generators[get_user_input(index) - 1]


def parse_supplied_arguments(run_profile: RunProfile, supplied_arguments: List[str]) -> Dict[str, str]:
    index = 0
    index_upper_bound = len(supplied_arguments)
    profile_specific_arguments = run_profile.get_arguments()
    result: Dict[str, str] = {}
    while index < index_upper_bound:
        argument = supplied_arguments[index]
        if profile_specific_arguments.__contains__(argument):
            if index + 1 >= index_upper_bound:
                print('\033[91m' + "Argument '" + argument + "' expects a following input." + '\033[0m')
            else:
                result[argument] = supplied_arguments[index + 1]
                index += 1
        else:
            print('\033[91m' + "Unrecognised argument '" + argument + "'" + '\033[0m')
        index += 1
    return result


def main():
    args = sys.argv[1:]

    run_profile: RunProfile = HelpRunProfile()
    try:
        profile_argument = args[0]
        for profile in run_profiles:
            if profile_argument == profile.command():
                run_profile = profile
                break

        supplied_arguments: Dict[str, str] = parse_supplied_arguments(run_profile, args[1:])

        illegal_characters = get_illegal_characters("illegal_characters.txt")
        print("Using illegal character set: ", illegal_characters)

        schema = choose_schema_generator().generate_schema(illegal_characters)

        run_profile.run(schema, supplied_arguments)
    except IndexError:
        run_profile.run({}, {})


schema_generators: List[SchemaGenerator] = [
    UnicodeSchemaGenerator()
]

run_profiles: List[RunProfile] = [
    HelpRunProfile(),
    SingleFileRewriteRunProfile(),
    BulkFileRewriteRunProfile()
]

main()

