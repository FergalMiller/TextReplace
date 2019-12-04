from abstract.SchemaGenerator import SchemaGenerator
from unicode_utils.UnicodeEscapeSchemaGenerator import UnicodeSchemaGenerator
import sys


def show_help():
    # TODO
    print("--Help content-- todo")


def bulk_file_rewrite(input_arguments: dict):
    # TODO
    print("todo")


def single_file_rewrite(input_arguments: dict):
    # TODO
    print("todo")


def main():
    args = sys.argv[1:]

    user_parameterised_arguments = {}
    run_profile = -1

    index = 0
    index_upper_bound = len(args)
    while index < index_upper_bound:
        argument = args[index]
        if run_profile_arguments.__contains__(argument):
            if run_profile < 0:
                run_profile = run_profile_arguments[argument][1]
            else:
                print('\033[91m' + "Cannot accept argument " + argument +
                      ". Run profile already selected." + '\033[0m')
        elif parameterised_arguments.keys().__contains__(argument):
            if index + 1 >= index_upper_bound:
                print('\033[91m' + "Argument '" + argument + "' expects a following input for "
                      + parameterised_arguments[argument][0] + '\033[0m')
            else:
                user_parameterised_arguments[argument] = args[index + 1]
                index += 1
        else:
            print("Unrecognised argument '" + argument + "'")
        index += 1


# Key = prefix
# Value = Tuple pair
#   pair[0] = Argument hint
#   pair[1] = Associated run profile
parameterised_arguments = {
    "-f": ("File path (single file rewrite)", 1),
    "-e": ("File extensions to match (bulk rewrite)", 2),
    "-r": ("Regex pattern for file names (bulk rewrite)", 2),
    "-d": ("Directory to be traversed (bulk rewrite)", 2)}
# Key = prefix
# Value = Tuple
#   tuple[0] = Argument hint
#   tuple[1] = Associated run profile
#   tuple[2] = Associated function call
run_profile_arguments = {
    "-h": ("Help", 0, show_help),
    "-s": ("Single file rewrite", 1, single_file_rewrite),
    "-b": ("Bulk file rewrite", 2, bulk_file_rewrite)}

main()

