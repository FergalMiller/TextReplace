from typing import Dict

from text_replace.common.profile.file_rewrite_profiles.unicode_replacer.unicode_escape_schema_generator import \
    UnicodeSchemaGenerator


def test_generate_schema():
    illegal_characters = set()
    illegal_characters.add('ä')
    illegal_characters.add('ö')
    illegal_characters.add('ü')

    schema: Dict[str, str] = UnicodeSchemaGenerator.generate_schema(illegal_characters)

    assert schema['ä'] == '\\u00e4'
    assert schema['ö'] == '\\u00f6'
    assert schema['ü'] == '\\u00fc'
