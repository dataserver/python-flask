class ErrorFormData(Exception):
    def __init__(self, message, errors=None, redirect_to=None):
        self.message = message
        self.errors = errors
        self.redirect_to = redirect_to

    def __str__(self):
        return self.message


class ErrorInvalidCredentials(Exception):
    def __init__(self, message, errors=None, redirect_to=None):
        self.message = message
        self.errors = errors
        self.redirect_to = redirect_to

    def __str__(self):
        return self.message


class ErrorNotAdministrator(ErrorInvalidCredentials):
    pass
