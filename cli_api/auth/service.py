"""
Service methods for handling authentication.
"""
from .interface import UserInterface
from .model import User, TokenBlacklist

from cli_api.extensions import db, bcrypt
from cli_api.common.errors import ServerException, UserException


class UserService:
    @staticmethod
    def register_user(user_obj: UserInterface) -> User:
        """
        Register a user.
        """
        try:
            user = User(email=user_obj["email"], password=user_obj["password"])

            db.session.add(user)
            db.session.commit()

            return user
        except Exception:
            raise ServerException("Unable to register user")

    @staticmethod
    def login_user(user_obj: UserInterface) -> str:
        """
        Login an already-registered user.

        :return: An authorization token
        """
        email = user_obj["email"]
        password = user_obj["password"]
        user = User.query.filter_by(email=email).first()

        # No user registered under given email
        if not user:
            raise UserException(
                f"Unable to find user with email '{email}'", status_code=404
            )

        check_password = bcrypt.check_password_hash(user.password, password)
        if not check_password:
            raise UserException(
                f"Invalid password for user with email '{email}'", status_code=403
            )

        try:
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                return auth_token
        except Exception:
            raise ServerException("Unable to generate login token, please try again")

    @staticmethod
    def logout_user(auth_token: str):
        """
        Logout user with given token.

        :param auth_token: Authorization token.
        """
        User.decode_auth_token(auth_token)
        TokenBlacklistService.add_to_blacklist(auth_token)


class TokenBlacklistService:
    """
    Service class for manipulating the token_blacklist table.
    """

    @staticmethod
    def add_to_blacklist(token: str):
        try:
            blacklist_token = TokenBlacklist(token)
            db.session.add(blacklist_token)
            db.session.commit()
        except Exception:
            raise ServerException("Unable to blacklist given token")
