#!/usr/bin/env python3
"""auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash password using bcrypt
    """
    salt = bcrypt.gensalt()
    encoded_password = password.encode("utf-8")

    return bcrypt.hashpw(encoded_password, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user
        """
        try:
            self._db.find_user_by(email=email)

            message = "User {} already exists".format(email)
            raise ValueError(message)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """check user credentials
        """
        try:
            user = self._db.find_user_by(email=email)

            encoded_password = password.encode("utf-8")

            return bcrypt.checkpw(encoded_password, user.hashed_password)
        except Exception:
            return False
