class Argument:
    key: str
    hint: str
    required: bool
    value: str

    def __init__(self, prefix, hint, required):
        self.key = prefix
        self.hint = hint
        self.required = required
        self.value = ""

    def __eq__(self, other: str):
        return self.key == other


class ArgumentError(Exception):
    reason: str

    def __init__(self, reason):
        super()
        self.reason = reason
