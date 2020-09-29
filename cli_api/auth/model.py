import datetime
import os

import flask
import jwt
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from cli_api.extensions import db, bcrypt
from cli_api.common.errors import UserException


class User(db.Model):
    """
    Model representing users.

    :param id: Auto-generated primary key
    :param email: User's email.
    :param password: A hash of the user's password
    :param registered_on: Date of user registration
    :param admin: Boolean flag representing whether the user is an admin or not
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, flask.current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id: int):
        """
        Generates an auth token.
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=0, seconds=60 * 30),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }

            return jwt.encode(
                payload, flask.current_app.config.get("SECRET_KEY"), algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str) -> int:
        """
        Decode an auth token.

        :param auth_token: An auth token.
        :returns: A user ID.
        """
        try:
            payload = jwt.decode(
                auth_token,
                flask.current_app.config.get("SECRET_KEY"),
                algorithms=["HS256"],
            )
            return payload["sub"]
        except jwt.ExpiredSignature:
            raise UserException(
                "Signature expired, please log in again", status_code=403
            )
        except jwt.InvalidTokenError:
            raise UserException("Invalid token, please log in again", status_code=403)


class TokenBlacklist(db.Model):
    """
    Model representing blacklisted JWT tokens.

    :param id: Auto-generated primary_key
    :param token: JWT token string
    :param blacklisted_on: Date that the token was blacklisted
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(512), unique=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)

    def __init__(self, token: str):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()
