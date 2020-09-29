from flask import request

from cli_api.common.errors import UserException


def get_bearer_token() -> str:
    """
    Get a bearer token from request headers.

    :return: A string token.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise UserException("Missing authorization token", status_code=403)

    auth_token = auth_header.split(" ")[1]
    return auth_token
