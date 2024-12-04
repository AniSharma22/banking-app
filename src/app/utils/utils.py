from bcrypt import hashpw, checkpw, gensalt


class Utils:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        """
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hashed password.
        """
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
