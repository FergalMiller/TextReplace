#!/usr/bin/python

import re
from typing import List, Type

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from text_replace.common.profile.abstract.file_rewrite_profile import FileRewriteProfile
from text_replace.common.profile.abstract.profile import Profile
from text_replace.common.profile.abstract.run_profile import RunProfile
from text_replace.common.profile.argument.argument_error import ArgumentError
from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_replacer_rewrite_profile import \
    RegexReplacerRewriteProfile
from text_replace.common.profile.file_rewrite_profiles.unicode_replacer.unicode_replacer_rewrite_profile import \
    UnicodeReplacerRewriteProfile
from text_replace.common.profile.run_profiles.bulk_file_run_profile import BulkFileRunProfile
from text_replace.common.profile.run_profiles.single_file_run_profile import SingleFileRunProfile


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


def generate_argument_toolbar(profile: Type[Profile]) -> str:
    arguments = profile.get_static_arguments()
    num_of_arguments = len(arguments)
    toolbar_text = ""
    i = 0
    while i < num_of_arguments:
        argument = arguments[i]
        if i > 0:
            toolbar_text += '\n'
        toolbar_text += argument.key + ": " + argument.hint
        i += 1
    return toolbar_text


def prompt_get_profile_arguments(profile: Type[Profile]) -> str:
    arguments = profile.get_static_arguments()
    argument_keys: List[str] = []
    for argument in arguments:
        argument_keys.append(argument.key)
    return prompt("Please enter the string of arguments you would like to supply the profile: ",
                  completer=WordCompleter(argument_keys),
                  bottom_toolbar=generate_argument_toolbar(profile))


def main():
    run_profile = prompt_run_profile()

    while True:
        try:
            run_profile_arguments = prompt_get_profile_arguments(run_profile)
            run_profile = run_profile(run_profile_arguments)
            break
        except ArgumentError as e:
            print('\033[91m' + e.reason + '\033[0m')

    file_rewrite_profile = prompt_file_rewrite_profile()
    file_rewrite_profile_arguments = prompt_get_profile_arguments(file_rewrite_profile)
    file_rewrite_profile = file_rewrite_profile(file_rewrite_profile_arguments)

    run_profile.run(file_rewrite_profile)


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
