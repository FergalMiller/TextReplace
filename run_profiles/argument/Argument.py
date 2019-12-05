class Argument:
    prefix: str
    hint: str

    def __init__(self, prefix, hint):
        self.prefix = prefix
        self.hint = hint

    def __eq__(self, other: str):
        return self.prefix == other
