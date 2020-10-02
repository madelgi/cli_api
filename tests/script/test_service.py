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


def test_execute(db: SQLAlchemy):
    obj1 = dict(
        name="echo_hello",
        user=1,
        content='sleep 30;'
    )


