import pytest
from models import Coin, Duty
from pg_db_connection import pg_db
from utils.helper_functions import clear_tables


@pytest.fixture
def populated_db():
    automate_coin = Coin.create(name="Automate")
    assemble_coin = Coin.create(name="Assemble")
    duty = Duty.create(name="Duty 4")

    return {
        "coins": [automate_coin, assemble_coin],
        "duties": [duty],
    }


def test_clear_tables_removes_all_rows(populated_db):
    assert Coin.select().count() == 2
    assert Duty.select().count() == 1

    clear_tables()

    assert Coin.select().count() == 0
    assert Duty.select().count() == 0