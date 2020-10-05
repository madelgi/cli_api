from unittest.mock import patch, MagicMock

from flask_sqlalchemy import SQLAlchemy

from cli_api.script.model import Script
from cli_api.script.service import ScriptService


def test_get_all_by_user(db: SQLAlchemy):
    script1 = Script(name="script_1", user=1, version=1, content='echo "HELLO"')
    script2 = Script(name="script_2", user=1, version=1, content='echo "HELLO"')
    db.session.add(script1)
    db.session.add(script2)
    db.session.commit()

    results = ScriptService.get_all_by_user(1)
    assert len(results) == 2
    assert script1 in results
    assert script2 in results


def test_get_by_user(db: SQLAlchemy):
    script1 = Script(name="script_1", user=1, version=1, content='echo "HELLO"')
    script2 = Script(name="script_1", user=1, version=2, content='echo "HELLO"')
    db.session.add(script1)
    db.session.add(script2)
    db.session.commit()

    # Default, get most recent
    result = ScriptService.get_script_by_user_and_name(1, "script_1")
    assert script2 == result

    # Get earlier version
    result = ScriptService.get_script_by_user_and_name(1, "script_1", version=1)
    assert script1 == result


def test_create(db: SQLAlchemy):
    obj1 = dict(
        name="echo_hello",
        user=1,
        content='echo "HELLO"',
    )

    obj2 = dict(
        name="echo_hello",
        user=1,
        content='#!/usr/bin/env bash\necho "HELLO"',
    )

    ScriptService.create(obj1)
    ScriptService.create(obj2)

    results = sorted(ScriptService.get_all_by_user(1), key=lambda x: x.version)
    assert len(results) == 2

    for k in obj1.keys():
        assert getattr(results[0], k) == obj1[k]

    for k in obj2.keys():
        assert getattr(results[1], k) == obj2[k]

    # Check versioning
    assert results[0].version == 1
    assert results[1].version == 2


def test_execute(monkeypatch, db: SQLAlchemy):
    job_service = MagicMock()
    redis_service = MagicMock()
    redis_service.submit_job = MagicMock(return_value=1)
    redis_service.commit_job_result = MagicMock()
    monkeypatch.setattr("cli_api.script.service.JobRedisService", redis_service)
    monkeypatch.setattr("cli_api.script.service.JobService", job_service)

    obj1 = dict(
        name="echo_hello",
        user=1,
        content='echo "HELLO"',
    )
    placeholder_dict = {'var1': 'val1', 'var2': 'val2'}
    ScriptService.create(obj1)

    ScriptService.execute(
        1, 'echo_hello', version=1, description="Running echo_hello!", placeholder_dict=placeholder_dict
    )

    # Confirm correct communication with redis/job service
    redis_service.submit_job.assert_called_with("echo \"HELLO\"", placeholder_dict)
    redis_service.commit_job_result.assert_called_with(1)
    job_service.create_job.assert_called_with(
        {'id': 1, 'user_id': 1, 'name': 'echo_hello', 'description': 'Running echo_hello!'}
    )
