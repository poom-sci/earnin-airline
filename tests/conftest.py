import os
import pytest
from sqlalchemy import text

from earnin_airline.db import DB


# create mock database for testing
test_db = DB()

@pytest.fixture(scope="function")
def override_db():
    import earnin_airline.db as db_module
    db_module.db = test_db
    return test_db


# clean up database after each test
@pytest.fixture(autouse=True)
def cleanup_db():
    yield
    with test_db.session() as session:
        session.execute(text("DELETE FROM passengers"))
        session.execute(text("DELETE FROM customers"))
        session.commit()