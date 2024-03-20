#!/usr/bin/env python3
"""basic auth module"""
from api.v1.auth.auth import Auth
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
