class APIError(Exception):
    def __init__(self, status, message=''):
        super().__init__(message)
        self.status = status


class CLIError(Exception):
    pass
