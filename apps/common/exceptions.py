class ApplicationError(Exception):
    def __init__(self, message: str, extra: dict[str, str] | None = None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}
