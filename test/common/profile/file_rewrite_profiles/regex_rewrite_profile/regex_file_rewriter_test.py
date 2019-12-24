import re
from typing import List

from test.test_utils import TestUtils
from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_file_rewriter import RegexFileRewriter
from text_replace.common.profile.file_rewrite_profiles.regex_replacer.regex_rewrite_command import RegexRewriteCommand

resource_file_path: str = TestUtils.get_resource_path()


def setup_module():
    TestUtils.create_resource_file()


def teardown_module():
    TestUtils.destroy_resource_file()


def generate_rewriter(pattern: str, rewrite_commands: List[str], arguments: List[str]) -> RegexFileRewriter:
    pattern = re.compile(pattern)
    parsed_rewrite_commands: List[RegexRewriteCommand] = []
    for rewrite_command in rewrite_commands:
        parsed_rewrite_command = RegexRewriteCommand.generate_rewrite_command(rewrite_command, arguments)
        parsed_rewrite_commands.append(parsed_rewrite_command)
    return RegexFileRewriter(pattern, parsed_rewrite_commands)


def test_modify_match_with_group():
    rewriter: RegexFileRewriter = generate_rewriter(r'\w(\w*)\w', ['1(0)'], [])
    full_match = "bin"
    modified = rewriter.modify_match(full_match)
    assert modified == "bbinn"


def test_modify_match_with_argument():
    rewriter: RegexFileRewriter = generate_rewriter(r'\w(\w*)\w', ['1({0})'], ['o'])
    full_match = "bin"
    modified = rewriter.modify_match(full_match)
    assert modified == "bon"


def test_modify_match_with_chained_argument_commands():
    rewriter: RegexFileRewriter = generate_rewriter(r'(he|good)(llo)', ['1({0})', '2({1})'], ['good', 'bye'])
    full_match = "hello"
    result = rewriter.modify_match(full_match)
    assert result == "goodbye"


def test_modify_match_with_chained_group_commands():
    rewriter: RegexFileRewriter = generate_rewriter(r'(he|llo)(llo)', ['1(2)', '2(1)'], [])
    full_match = "hello"
    result = rewriter.modify_match(full_match)
    assert result == "llollo"


def test_modify_match_with_chained_mixed_commands():
    rewriter: RegexFileRewriter = generate_rewriter(r'(c|br)ow()', ['1({0})', '2(1)'], ['br'])
    full_match = "cow"
    result = rewriter.modify_match(full_match)
    assert result == "browbr"


def test_modify_match_with_group_that_may_exist():
    rewriter: RegexFileRewriter = generate_rewriter(r'hello(\.)?', ['1({0})'], ['!'])
    full_match = "hello"
    result = rewriter.modify_match(full_match)
    assert result == "hello"

    full_match = "hello."
    result = rewriter.modify_match(full_match)
    assert result == "hello!"


def test_modify_match_swap():
    rewriter: RegexFileRewriter = \
        generate_rewriter(r'(these()?)?()swap((\s)?these)?', ['5({0})', '3(4)', '4({0})', '2({1})'], ['', ' '])
    full_content = "swap these"
    result = rewriter.recursive_match_result(full_content)
    assert result == "these swap"


def test_recursive_replace():
    rewriter: RegexFileRewriter = generate_rewriter(r'o', ['0({0})'], ['!'])
    full_content = "hello for I am on my way to the house"
    result = rewriter.recursive_match_result(full_content)
    assert result == "hell! f!r I am !n my way t! the h!use"


def test_recursive_replace_swap():
    rewriter: RegexFileRewriter = \
        generate_rewriter(r'(these()?)?()swap((\s)?these)?', ['5({0})', '3(4)', '4({0})', '2({1})'], ['', ' '])
    full_content = "i would like to swap these words"
    result = rewriter.recursive_match_result(full_content)
    assert result == "i would like to these swap words"


def test_recursive_replace_with_group_that_may_exist():
    rewriter: RegexFileRewriter = generate_rewriter(r'hello(\.)?', ['1({0})'], ['!'])
    full_content = "hello words. hello. more words"
    result = rewriter.recursive_match_result(full_content)
    assert result == "hello words. hello! more words"


def test_rewriter_with_arguments():
    rewriter: RegexFileRewriter = generate_rewriter(r'^\w(\w*)\w$', ['1({0})'], ['middle'])

    TestUtils.overwrite_resource_file_content("bing")

    rewriter.rewrite_file(resource_file_path)

    content = TestUtils.fetch_resource_file_content()
    assert content == "bmiddleg"
