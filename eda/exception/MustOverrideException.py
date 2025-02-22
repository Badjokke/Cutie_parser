class MustOverrideException(RuntimeError):
    def __init__(self, message):
        super(MustOverrideException, self).__init__(message)