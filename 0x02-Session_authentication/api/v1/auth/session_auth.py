#!/usr/bin/env python3
"""Authorization class for API"""
import base64
from api.v1.auth.auth import Auth
from flask import request
from models.user import User
from typing import List, TypeVar


class BasicAuth(Auth):
    """BasicAuth class definition
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract base64 authorization header"""
        if authorization_header is None:
            return (None)
        if type(authorization_header) != str:
            return (None)
        if authorization_header.startswith('Basic ') is False:
            return (None)
        return (authorization_header[6:])

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Base64 decoding
        """
        if base64_authorization_header is None:
            return (None)
        if type(base64_authorization_header) != str:
            return (None)
        try:
            decoded = base64.decodebytes(
                    base64_authorization_header.encode('utf-8'))
        except Exception:
            return (None)
        try:
            return (decoded.decode('utf-8'))
        except Exception:
            return (None)

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials from decoded string
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        info = decoded_base64_authorization_header.split(':')
        user = info[0]
        info = info[1:]
        return (user, ":".join(info))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Obtain user's identity using credentials"""
        if user_email is None or type(user_email) != str:
            return (None)
        if user_pwd is None or type(user_pwd) != str:
            return (None)
        result = User.search({'email': user_email})
        if len(result) == 0:
            return (None)
        else:
            the_user = result[0]
            if the_user.is_valid_password(user_pwd):
                return (the_user)
            return (None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Return current User instance
        """
        header = self.authorization_header(request)
        ex_str = self.extract_base64_authorization_header(header)
        dec_str = self.decode_base64_authorization_header(ex_str)
        cred = self.extract_user_credentials(dec_str)
        user_obj = self.user_object_from_credentials(cred[0], cred[1])
        return (user_obj)
