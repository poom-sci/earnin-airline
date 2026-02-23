import os
import pytest
from sqlalchemy import text

from earnin_airline.db import DB

test_db = DB()

@pytest.fixture(scope="function")
def override_db():
    import earnin_airline.db as db_module
    db_module.db = test_db
    return test_db


@pytest.fixture(autouse=True)
def setup_and_cleanup_db():
    with test_db.session() as session:
        session.execute(text(
            "INSERT INTO flights (id, departure_time, arrival_time, departure_airport, arrival_airport, departure_timezone, arrival_timezone) "
            "VALUES ('AAA01', '2024-12-01T00:00:00Z', '2024-12-01T02:00:00Z', 'DMK', 'HYD', 'Asia/Bangkok', 'Asia/Bangkok') "
            "ON CONFLICT (id) DO NOTHING"
        ))
        session.commit()
    
    yield
    
    with test_db.session() as session:
        session.execute(text("DELETE FROM passengers"))
        session.execute(text("DELETE FROM customers"))
        session.execute(text("DELETE FROM flights"))
        session.commit()