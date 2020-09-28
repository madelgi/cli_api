import datetime
from unittest.mock import patch

from flask.testing import FlaskClient

from cli_api.auth.model import User
from cli_api.auth.service import UserService


@patch.object(
    UserService, "register_user", lambda register_req: User(**register_req)
)
def test_register_user(client: FlaskClient):
    with client:
        payload = {
            'email': 'max@gmail.com',
            'password': 'abc123'
        }

        result = client.post("/auth/register", json=payload).get_json()
        assert result['email'] == 'max@gmail.com'
        assert result['registered_on']
