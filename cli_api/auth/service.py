"""
Service methods for handling authentication.
"""
from .interface import UserInterface
from .model import User, TokenBlacklist

from cli_api.extensions import db, bcrypt


class UserService:

    @staticmethod
    def register_user(user_obj: UserInterface):
        """
        Register a user.
        """
        user = User(
            email=user_obj['email'],
            password=user_obj['password']
        )

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def login_user(user_obj: UserInterface):
        """
        Login an already-registered user.
        """
        email = user_obj['email']
        password = user_obj['password']

        user = User.query.filter_by(email=email).first()

        # No user registered under given email
        if not user:
            response_object = {
                "ok": False,
                "message": f"Unable to find user with email '{email}'"
            }

            return response_object, 400

        check_password = bcrypt.check_password_hash(user.password, password)
        if not check_password:
            response_object = {
                "ok": False,
                "message": f"Invalid password for user with email '{email}'"
            }

            return response_object, 400

        try:
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    "ok": True,
                    "message": "Successfully logged in",
                    "auth_token": auth_token
                }

                return response_object, 200
        except Exception:
            response_object = {
                "ok": False,
                "message": "Unable to generate login token, please try again"
            }

            return response_object, 500


class TokenBlacklistService:
    """
    Service class for manipulating the token_blacklist table.
    """

    @staticmethod
    def add_to_blacklist(token: str):
        blacklist_token = TokenBlacklist(token)
        db.session.add(blacklist_token)
        db.session.commit()
