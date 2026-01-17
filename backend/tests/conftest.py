import pytest
from pg_db_connection import pg_db
from utils.helper_functions import clear_tables
from app import app as flask_app

@pytest.fixture(autouse=True)
def clean_database():
    pg_db.connect()
    clear_tables()
    yield
    pg_db.close()

@pytest.fixture
def app():
    flask_app.config.update(TESTING=True)
    return flask_app

@pytest.fixture()
def client(app):
    return app.test_client()