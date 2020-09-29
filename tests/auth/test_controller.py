from unittest.mock import patch

from cli_api.auth.model import User
from cli_api.auth.service import UserService


@patch.object(UserService, "register_user", lambda register_req: User(**register_req))
def test_register_user_success(app):
    with app.test_client() as client:
        payload = {"email": "max@gmail.com", "password": "abc123"}

        result = client.post("/auth/register", json=payload)
        assert result.status_code == 201

        result_json = result.get_json()
        assert result_json["email"] == "max@gmail.com"
        assert result_json["registered_on"]


@patch.object(UserService, "login_user", lambda register_req: b"token123")
def test_login_success(app):
    with app.test_client() as client:
        payload = {"email": "max@gmail.com", "password": "abc123"}

        result = client.post("/auth/login", json=payload)
        assert result.status_code == 200

        result_json = result.get_json()
        assert result_json["message"] == "Successfully logged in"
        assert result_json["auth_token"] == "token123"


def test_logout_no_token(app):
    with app.test_client() as client:
        result = client.post("/auth/logout")
        assert result.status_code == 403

        assert result.get_json()["message"] == "Missing authorization token"


@patch.object(UserService, "logout_user", lambda _: None)
def test_logout_success(app):
    with app.test_client() as client:
        headers = {"Authorization": "Bearer abc123"}
        result = client.post("/auth/logout", headers=headers)

        assert result.status_code == 200

        result_json = result.get_json()
        assert result_json["message"] == "Successfully logged out"
        assert result_json["auth_token"] == "abc123"
