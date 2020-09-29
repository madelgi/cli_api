from unittest.mock import patch

from cli_api.script.model import Script
from cli_api.auth.model import User
from cli_api.script.service import ScriptService


@patch.object(ScriptService, 'create', lambda req: None)
def test_create_script_no_token(app):
    with app.test_client() as client:
        payload = {"name": "script_1", "content": "echo \"HELLO\""}
        res = client.post("/scripts", json=payload)

        assert res.status_code == 403
        assert res.get_json()["message"] == "Missing authorization token"


@patch.object(User, 'decode_auth_token', lambda _: 1)
@patch('cli_api.script.service.ScriptService.create')
def test_create_script_success(script_create, app):
    with app.test_client() as client:
        payload = {"name": "script_1", "content": "echo \"HELLO\""}
        headers = {"Authorization": "Bearer abc123"}
        script_create.return_value = Script(
            name=payload['name'],
            content=payload['content'],
            user=1,
            version=1,
            id=1
        )
        res = client.post("/scripts", json=payload, headers=headers)

        payload["user"] = 1
        script_create.assert_called_with(payload)

        assert res.status_code == 201
        assert res.get_json()['user'] == 1
