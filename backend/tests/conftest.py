import pytest
from pg_db_connection import pg_db
from utils.helper_functions import clear_tables

@pytest.fixture(autouse=True)
def clean_database():
    pg_db.connect()
    clear_tables()
    yield
    pg_db.close()