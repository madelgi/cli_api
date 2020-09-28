from flask_sqlalchemy import SQLAlchemy

from cli_api.script.model import Script
from cli_api.script.service import ScriptService


def test_get_all_by_user(db: SQLAlchemy):
    script1 = Script(name='s1.sh', user='max', version=1)
    script2 = Script(name='s2.sh', user='max', version=1)
    db.session.add(script1)
    db.session.add(script2)
    db.session.commit()

    results = ScriptService.get_all_by_user('max')

    assert len(results) == 2
    assert script1 in results
    assert script2 in results


def test_get_by_user(db: SQLAlchemy):
    script1 = Script(name='s1.sh', user='max', version=1)
    script2 = Script(name='s1.sh', user='max', version=2)
    db.session.add(script1)
    db.session.add(script2)
    db.session.commit()

    results = ScriptService.get_script_by_user_and_name(user='max', name='s1.sh')

    assert len(results) == 2
    assert script1 in results
    assert script2 in results


def test_create(db: SQLAlchemy):
    obj = dict(
        name='script.sh',
        user='max',
        content='#!/usr/bin/env bash\necho \"HELLO\"',
        version=1
    )

    ScriptService.create(obj)
    results = ScriptService.get_all_by_user('max')
    assert len(results) == 1

    for k in obj.keys():
        assert getattr(results[0], k) == obj[k]

    assert results[0].id == 1
