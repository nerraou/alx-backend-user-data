#!/usr/bin/env python3
"""DB module
"""
from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add user method
        """
        u = User(email=email, hashed_password=hashed_password)

        self._session.add(u)
        self._session.commit()
        return u

    def find_user_by(self, **kwargs: Dict) -> User:
        """find user by
        """
        user = self._session.query(User).filter_by(**kwargs).one()

        return user

    def update_user(self, user_id: int, **kwargs: Dict):
        """update user
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError()
            setattr(user, key, value)

        self._session.commit()
