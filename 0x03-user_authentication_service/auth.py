#!/usr/bin/env python3
"""_summary_
"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from typing import Union


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The salted hash of the password.
        """
    passwrd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(passwrd, salt)
    return hashed_pass


def _register_user(self, email: str, password: str) -> Union[None, User]:
    """Registers a new user with the given email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
    try:
        self.db.find_user_by(email=email)
        raise ValueError(f"User with {email} alreay exists")
    except NoResultFound:
        hashed_password = _hash_password(password)
        user = User(email=email, hashed_password=hashed_password)
        self._db.add_user(user)
        return user
    pass


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """_summary_
        """
        self._db = DB()
