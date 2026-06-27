import pytest

from database import create_table


@pytest.fixture()
def db_path(tmp_path):
    db_file = tmp_path / "test_inventory.db"
    create_table(db_file)
    return db_file
