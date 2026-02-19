class AppException(Exception):
    def __init__(self, status_code: int, message: str, code: str, details: dict | None = None):
        self.status_code = status_code
        self.message = message
        self.code = code
        self.details = details or {}
