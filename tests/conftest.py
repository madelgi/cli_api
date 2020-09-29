import pytest


from cli_api.app import create_app


@pytest.fixture
def app():
    return create_app("test")


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from cli_api.extensions import db

    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
