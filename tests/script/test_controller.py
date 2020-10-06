import datetime
import pytest
from unittest.mock import patch, MagicMock

from cli_api.jobs.model import Job
from cli_api.script.model import Script
from cli_api.auth.model import User
import cli_api.auth.model
from cli_api.script.service import ScriptService


@pytest.fixture
def login(monkeypatch):
    monkeypatch.setattr("cli_api.auth.model.User.decode_auth_token", MagicMock(return_value=1))


@patch.object(ScriptService, "create", lambda req: None)
def test_create_script_no_token(app):
    with app.test_client() as client:
        payload = {"name": "script_1", "content": 'echo "HELLO"'}
        res = client.post("/script", json=payload)

        assert res.status_code == 403
        assert res.get_json()["message"] == "Missing authorization token"


@patch.object(User, "decode_auth_token", lambda _: 1)
@patch("cli_api.script.service.ScriptService.create")
def test_create_script_success(script_create, app):
    with app.test_client() as client:
        payload = {"name": "script_1", "content": 'echo "HELLO"'}
        headers = {"Authorization": "Bearer abc123"}
        script_create.return_value = Script(
            name=payload["name"], content=payload["content"], user=1, version=1, id=1
        )
        res = client.post("/script", json=payload, headers=headers)

        payload["user"] = 1
        script_create.assert_called_with(payload)

        assert res.status_code == 201
        assert res.get_json()["user"] == 1


def test_get_script(app, login, monkeypatch):
    script_dict = {'name': 'script_1', 'content': 'echo \"HELLO\"', 'user': 1, 'version': 1, 'id': 1}
    script_service = MagicMock(get_script_by_user_and_name=MagicMock(return_value=Script(**script_dict)))
    monkeypatch.setattr("cli_api.script.controller.ScriptService", script_service)

    with app.test_client() as client:
        payload = {k: v for k, v in script_dict.items() if k in ['name', 'content']}
        headers = {"Authorization": "Bearer abc123"}
        res = client.get("/script/script_1", json=payload, headers=headers)
        assert 'placeholders' in res.get_json()
        assert all(item in res.get_json().items() for item in script_dict.items())


def test_get_script_placeholders(app, login, monkeypatch):
    script_dict = {'name': 'script_1', 'content': 'echo {{PLACEHOLDER_TEXT}} | wc -w', 'user': 1, 'version': 1, 'id': 1}
    script_service = MagicMock(get_script_by_user_and_name=MagicMock(return_value=Script(**script_dict)))
    monkeypatch.setattr("cli_api.script.controller.ScriptService", script_service)

    with app.test_client() as client:
        payload = {k: v for k, v in script_dict.items() if k in ['name', 'content']}
        headers = {"Authorization": "Bearer abc123"}
        res = client.get("/script/script_1", json=payload, headers=headers)
        assert 'placeholders' in res.get_json()
        assert ('PLACEHOLDER_TEXT', None) in res.get_json()['placeholders'].items()
        assert all(item in res.get_json().items() for item in script_dict.items())


@patch.object(User, "decode_auth_token", lambda _: 1)
@patch("cli_api.script.service.ScriptService.execute")
def test_execute_script(script_execute, app):
    with app.test_client() as client:
        payload = {"VAR1": "val1", "VAR2": "val2"}
        headers = {"Authorization": "Bearer abc123"}
        job_json = {
            "id": "1",
            "name": "job",
            "submit_time": None,
            "complete_time": None,
            "description": None,
            "user_id": 1,
            "complete": False,
            "results": None,
        }

        script_execute.return_value = Job(**job_json)
        res = client.post("/script/test_script/execute", json=payload, headers=headers)

        assert res.get_json() == job_json
        assert script_execute.called_with(1, "test_script", payload)
