#!/usr/bin/env python3
"""auth module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """hash password using bcrypt
    """
    salt = bcrypt.gensalt()
    encoded_password = password.encode("utf-8")

    return bcrypt.hashpw(encoded_password, salt)


def _generate_uuid() -> str:
    """generate uuid
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """create user session
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()

            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get user from session id
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
