import re

from text_replace.common.profile.argument.argument_error import ArgumentError


class Argument(object):
    """
    Argument encapsulates a single argument that may be used by a Profile object
    """
    key: str
    hint: str
    required: bool
    value: str
    value_pattern: str

    def __init__(self, prefix: str, hint: str, required: bool, value_pattern: str):
        self.key = prefix
        self.hint = hint
        self.required = required
        self.value = ""
        self.value_pattern = value_pattern

    def __eq__(self, other: str):
        return self.key == other

    def pass_value(self, value: str): self.value = value.strip()

    def has_value(self) -> bool: return self.value != ""

    def has_value_pattern(self) -> bool: return self.value_pattern != ""

    def self_validate(self):
        if self.required and not self.has_value():
            raise ArgumentError("Argument with key '" + self.key +
                                "' (" + self.hint + ") not valid, a value is required to be supplied.")
        if self.has_value_pattern() and self.has_value():
            if not re.match(self.value_pattern, self.value):
                raise ArgumentError("Value supplied to argument " + self.key +
                                    " (" + self.value + ") does not adhere to value regex pattern: " +
                                    self.value_pattern)
