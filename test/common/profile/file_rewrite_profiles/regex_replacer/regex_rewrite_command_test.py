import re

import pytest

from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_rewrite_command import RegexRewriteCommand


def test_init_with_non_existent_parameter():
    with pytest.raises(Exception):
        RegexRewriteCommand(0, ["{0}"], [])


def test_init_happy_path():
    RegexRewriteCommand(0, ["1", "{0}", "2"], ["val"])


# Replaces the first character in a word with the last character.
def test_get_replacement_1():
    command = RegexRewriteCommand(1, ["3"], [])
    pattern = re.compile(r'^(\w)(\w*)(\w)$')
    result = command.get_replacement("hello", pattern)
    assert result == "o"


# Replaces the whole string with multiple references to groups.
def test_get_replacement_2():
    command = RegexRewriteCommand(0, ["1", "3", "3", "1", "2"], [])
    pattern = re.compile(r'^(\w)(\w*)(\w)$')
    result = command.get_replacement("hello", pattern)
    assert result == "hoohell"


# Replaces the entire string with the word "goodbye"
def test_get_replacement_3():
    command = RegexRewriteCommand(0, ["{0}"], ["goodbye"])
    pattern = re.compile(r'^.*$')
    result = command.get_replacement("hello", pattern)
    assert result == "goodbye"

