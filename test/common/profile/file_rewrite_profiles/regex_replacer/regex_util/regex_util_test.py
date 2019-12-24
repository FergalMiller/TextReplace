import re

import pytest

from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_util.regex_util import RegexUtil, GroupMatch


@pytest.fixture(autouse=True)
def group_match() -> GroupMatch:
    pattern = re.compile(r'^(my)\s(pa(tt)ern)$')
    return RegexUtil.get_group_match("my pattern", pattern)


def test_get_group_match_values(group_match: GroupMatch):
    assert group_match.get_value_of_group(0) == "my pattern"
    assert group_match.get_value_of_group(1) == "my"
    assert group_match.get_value_of_group(2) == "pattern"
    assert group_match.get_value_of_group(3) == "tt"


def test_get_group_match_begin_positions(group_match: GroupMatch):
    assert group_match.get_begin_position_of_group(0) == 0
    assert group_match.get_begin_position_of_group(1) == 0
    assert group_match.get_begin_position_of_group(2) == 3
    assert group_match.get_begin_position_of_group(3) == 5


def test_get_group_match_end_positions(group_match: GroupMatch):
    assert group_match.get_end_position_of_group(0) == 10
    assert group_match.get_end_position_of_group(1) == 2
    assert group_match.get_end_position_of_group(2) == 10
    assert group_match.get_end_position_of_group(3) == 7
