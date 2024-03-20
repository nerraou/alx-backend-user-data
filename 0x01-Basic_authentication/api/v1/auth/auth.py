#!/usr/bin/env python3
"""auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check if path requres auth
        """
        if path is None or excluded_paths is None:
            return True

        path = path.strip("/")
        for excluded_path in excluded_paths:
            excluded_path = excluded_path.strip("/")

            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        returns authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        get current user from request
        """
        return None
