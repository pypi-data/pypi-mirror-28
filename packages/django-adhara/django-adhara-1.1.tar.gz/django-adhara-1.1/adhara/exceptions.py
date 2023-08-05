class AdharaException(Exception):
    pass


class InvalidInput(AdharaException):
    pass


class InvalidDatabaseSelected(AdharaException):
    pass


class UnAuthorizedException(AdharaException):
    pass
