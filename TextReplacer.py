#!/usr/bin/python

import re
from typing import Dict, List, Type

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from text_replace.common.profile.abstract.file_rewrite_profile import FileRewriteProfile
from text_replace.common.profile.abstract.profile import Profile
from text_replace.common.profile.abstract.run_profile import RunProfile
from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_replacer_rewrite_profile import \
    RegexReplacerRewriteProfile
from text_replace.common.profile.file_rewrite_profiles.unicode_replacer.unicode_replacer_rewrite_profile import \
    UnicodeReplacerRewriteProfile
from text_replace.common.profile.run_profiles.bulk_file_run_profile import BulkFileRunProfile
from text_replace.common.profile.run_profiles.single_file_run_profile import SingleFileRunProfile


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


def generate_profile_toolbar_text(profiles: List[Type[Profile]]) -> str:
    toolbar_text = ""
    num_of_profiles = len(profiles)
    i = 0
    while i < num_of_profiles:
        profile = profiles[i]
        profile_command = profile.command()
        profile_description = profile.description()
        if i > 0:
            toolbar_text += '\n'
        toolbar_text += profile_command + ": " + profile_description
        i += 1
    return toolbar_text


def match_run_profile(prefix: str) -> Type[RunProfile]:
    for profile in run_profiles:
        if prefix == profile.command():
            return profile
    raise Exception("No run profile with prefix " + prefix)


def prompt_run_profile() -> Type[RunProfile]:
    available_commands: List[str] = []
    for profile in run_profiles:
        available_commands.append(profile.command())
    user_input = prompt("Please enter the command for the run profile you would like to use: ",
                        completer=WordCompleter(available_commands),
                        bottom_toolbar=generate_profile_toolbar_text(run_profiles))
    try:
        return match_run_profile(user_input)
    except Exception as e:
        print('\033[91m' + e.__str__() + '\033[0m')
    return prompt_run_profile()


def match_file_rewrite_profile(prefix: str) -> Type[FileRewriteProfile]:
    for profile in file_rewrite_profiles:
        if prefix == profile.command():
            return profile
    raise Exception("No rewrite profile with prefix " + prefix)


def prompt_file_rewrite_profile() -> Type[FileRewriteProfile]:
    available_commands: List[str] = []
    for profile in file_rewrite_profiles:
        available_commands.append(profile.command())
    user_input = prompt("Please enter the command for the file rewrite profile you would like to use: ",
                        completer=WordCompleter(available_commands),
                        bottom_toolbar=generate_profile_toolbar_text(file_rewrite_profiles))
    try:
        return match_file_rewrite_profile(user_input)
    except Exception as e:
        print('\033[91m' + e.__str__() + '\033[0m')
    return prompt_file_rewrite_profile()


def prompt_get_profile_arguments(profile: Type[Profile]):
    arguments = profile.get_static_arguments()
    argument_keys: List[str] = []
    for argument in arguments:
        argument_keys.append(argument.key)


def main():
    run_profile = prompt_run_profile()
    file_rewrite_profile = prompt_file_rewrite_profile()

    print("Chosen")
    print(run_profile)
    print(file_rewrite_profile)
    '''
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
    '''


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
