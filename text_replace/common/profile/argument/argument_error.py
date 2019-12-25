class ArgumentError(Exception):
    reason: str

    def __init__(self, reason):
        super()
        self.reason = reason
