import pytest


from cli_api.auth.model import User


def test_user_create(db):
    user = User("max@gmail.com", "pass123", admin=True)
    assert user


def test_encode_auth_token(db):
    user = User("max@gmail.com", "pass123", admin=True)
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)


def test_decode_auth_token(db):
    user = User("max@gmail.com", "pass123", admin=True)
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    decoded = User.decode_auth_token(auth_token)
    assert decoded == user.id
