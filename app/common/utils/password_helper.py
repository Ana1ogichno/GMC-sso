from passlib.context import CryptContext

from app.common.contracts import IPasswordHelper


class PasswordHelper(IPasswordHelper):
    """
    Helper class for password hashing and verification using passlib's CryptContext.
    """

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies if the plain password matches the hashed password.

        :param plain_password: The plain-text password to verify.
        :param hashed_password: The hashed password to compare against.
        :return: True if passwords match, otherwise False.
        """

        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str | None) -> str | None:
        """
        Hashes the given password using bcrypt hashing scheme.

        :param password: The plain-text password to hash.
        :return: The hashed password if password is not None, otherwise None.
        """

        if password is None:
            return None
        return self.pwd_context.hash(password)
