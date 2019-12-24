from typing import Dict

from test.test_utils import TestUtils
from text_replace.common.file_rewriters.line_by_line_rewriter import LineByLineRewriter

resource_file_path = "TEST_RESOURCE_TEMP.txt"
schema: Dict[str, str] = {
        "dog": "cat",
        "mine": "yours",
        "red": "blue"
}


def setup_module():
    TestUtils.create_resource_file(resource_file_path)


def teardown_module():
    TestUtils.destroy_resource_file(resource_file_path)


def prepare_text_content(content: str):
    TestUtils.overwrite_resource_file_content(resource_file_path, content)


def test_rewrite_with_multiple_matches():
    prepare_text_content("I like that dog\nmine is red")
    LineByLineRewriter.rewrite(resource_file_path, schema)

    content = TestUtils.fetch_resource_file_content(resource_file_path)
    assert content == "I like that cat\nyours is blue"


def test_rewrite_with_no_matches():
    original_and_expected = "I like elephants\nhis is green"
    prepare_text_content(original_and_expected)
    LineByLineRewriter.rewrite(resource_file_path, schema)

    content = TestUtils.fetch_resource_file_content(resource_file_path)
    assert content == original_and_expected
