#!/usr/bin/env python3
"""auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password using bcrypt
    """
    salt = bcrypt.gensalt()
    encoded_password = password.encode("utf-8")

    return bcrypt.hashpw(encoded_password, salt)
