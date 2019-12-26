#!/usr/bin/python

import re
import sys
from typing import Dict, List, Type

from text_replace.common.profile.abstract.file_rewrite_profile import FileRewriteProfile
from text_replace.common.profile.abstract.run_profile import RunProfile
from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_replacer_rewrite_profile import \
    RegexReplacerRewriteProfile
from text_replace.common.profile.file_rewrite_profiles.unicode_replacer.unicode_replacer_rewrite_profile import \
    UnicodeReplacerRewriteProfile
from text_replace.common.profile.run_profiles.bulk_file_run_profile import BulkFileRunProfile
from text_replace.common.profile.run_profiles.single_file_run_profile import SingleFileRunProfile


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


def match_run_profile_type(prefix: str) -> Type[RunProfile]:
    for profile in run_profiles:
        if prefix == profile.command():
            return profile
    raise Exception("No run profile with prefix ", prefix)


def match_file_rewrite_profile_type(prefix: str) -> Type[FileRewriteProfile]:
    for profile in file_rewrite_profiles:
        if prefix == profile.command():
            return profile
    raise Exception("No rewrite profile with prefix ", prefix)


def main():
    command = " ".join(sys.argv[1:])
    print("Command:", command)
    command_search = command_pattern.search(command)

    run_profile_prefix: str = ""
    run_profile_args: str = ""
    rewrite_profile_prefix: str = ""
    rewrite_profile_args: str = ""

    if command_search:
        run_profile_prefix = command_search.group(1)
        run_profile_args = command_search.group(2)
        rewrite_profile_prefix = command_search.group(3)
        rewrite_profile_args = command_search.group(4)
    else:
        # TODO: Handle this
        exit(20)

    run_profile_type: Type[RunProfile] = match_run_profile_type(run_profile_prefix)
    rewrite_profile_type: Type[FileRewriteProfile] = match_file_rewrite_profile_type(rewrite_profile_prefix)

    run_profile: RunProfile = run_profile_type(run_profile_args)
    rewrite_profile: FileRewriteProfile = rewrite_profile_type(rewrite_profile_args)

    run_profile.run(rewrite_profile)


command_pattern = re.compile(r'(-[a-z]+)\[(.*)\]\s*(-[a-z]+)\[(.*)\]')

run_profiles: List[Type[RunProfile]] = [
    SingleFileRunProfile,
    BulkFileRunProfile
]

file_rewrite_profiles: List[Type[FileRewriteProfile]] = [
    UnicodeReplacerRewriteProfile,
    RegexReplacerRewriteProfile
]

main()
