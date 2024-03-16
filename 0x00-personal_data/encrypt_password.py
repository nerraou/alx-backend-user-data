#!/usr/bin/env python3
"""
encrypt passwords
"""
import bcrypt


def hash_password(password: str) -> str:
    """hash password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
