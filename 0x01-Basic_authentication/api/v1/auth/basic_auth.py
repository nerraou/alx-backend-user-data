#!/usr/bin/env python3
"""basic auth module"""
from api.v1.auth.auth import Auth


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
