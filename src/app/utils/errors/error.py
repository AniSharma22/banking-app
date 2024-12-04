class UserError(Exception):
    """Base exception class for all user-related errors"""
    pass


class UserExistsError(UserError):
    """Raised when attempting to create a user that already exists"""

    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists")


class InvalidCredentialsError(UserError):
    """ Raised when invalid credentials are entered (email or password) """

    def __init__(self, message: str):
        super().__init__(f"{message}")

class DatabaseError(Exception):
    """Base exception class for all database-related errors"""
    def __init__(self, message: str):
        super().__init__(message)