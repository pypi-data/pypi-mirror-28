class BaseError(Exception):
    def __init__(self, message: str):
        self.message = message


class WrongContentType(BaseError):
    def __init__(self):
        self.message = "Wrong content type! Supported are list, str, Tag"


class WrongValidatorCall(BaseError):
    def __init__(self):
        self.message = "Validator call can have 1 or 2 params."
