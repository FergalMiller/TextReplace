import os
from typing import Dict

from text_replace.common.file_rewriters.line_by_line_rewriter import LineByLineRewriter

resource_path = "TEST_RESOURCE_TEMP.txt"
schema: Dict[str, str] = {
        "dog": "cat",
        "mine": "yours",
        "red": "blue"
}


def setup_module(module):
    open(resource_path, 'w').close()


def teardown_module(module):
    os.remove(resource_path)


def prepare_text_content(content: str):
    with open(resource_path, 'w') as resource:
        resource.write(content)


def test_rewrite_with_multiple_matches():
    prepare_text_content("I like that dog\nmine is red")
    LineByLineRewriter.rewrite(resource_path, schema)

    with open(resource_path, 'r') as resource:
        assert resource.read().__eq__("I like that cat\nyours is blue")


def test_rewrite_with_no_matches():
    content = "I like elephants\nhis is green"
    prepare_text_content(content)
    LineByLineRewriter.rewrite(resource_path, schema)

    with open(resource_path, 'r') as resource:
        assert resource.read().__eq__(content)
