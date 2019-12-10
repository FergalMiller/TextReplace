class Argument:
    prefix: str
    hint: str
    required: bool

    def __init__(self, prefix, hint, required):
        self.prefix = prefix
        self.hint = hint
        self.required = required

    def __eq__(self, other: str):
        return self.prefix == other


class ArgumentError(Exception):
    reason: str

    def __init__(self, reason):
        super()
        self.reason = reason
