#!/usr/bin/env python3
"""basic auth module"""
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64
import binascii


class BasicAuth(Auth):
    """basic auth class"""

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """
        extract base64 from authorization header
        """
        if type(auth_header) is not str:
            return None
        prefix = "Basic "
        if not auth_header.startswith(prefix):
            return None
        return auth_header[len(prefix):]

    def decode_base64_authorization_header(self,
                                           base64_auth_header: str) -> str:
        """
        decode base64 authorization header
        """
        if type(base64_auth_header) is not str:
            return None
        try:
            decoded = base64.b64decode(s=base64_auth_header, validate=True)
            return decoded.decode("utf-8")
        except (binascii.Error, Exception):
            return None

    def extract_user_credentials(self,
                                 decoded_base64: str) -> Tuple[str, str]:
        """
        extract user credentials
        """
        if type(decoded_base64) is not str:
            return (None, None)

        if ":" not in decoded_base64:
            return (None, None)

        email, password = decoded_base64.split(":")

        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar("User"):
        """
        user object from credentials
        """
        if type(user_email) is not str or type(user_pwd) is not str:
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if len(users) == 0:
            return None

        if users[0].is_valid_password(user_pwd):
            return users[0]

        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        get current user from request
        """
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_base64 = self.decode_base64_authorization_header(base64_header)
        email, password = self.extract_user_credentials(decoded_base64)
        return self.user_object_from_credentials(email, password)
