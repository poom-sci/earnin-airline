import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy import text

from earnin_airline.app import app

class TestRetrieveFlight:
    
    def test_retrieve_flight_with_different_timezones(self, override_db):
        with override_db.session() as session:
            session.execute(text(
                "INSERT INTO flights (id, departure_time, arrival_time, departure_airport, arrival_airport, departure_timezone, arrival_timezone) "
                "VALUES ('LHR99', '2024-12-15T10:00:00Z', '2024-12-15T18:00:00Z', 'LHR', 'BKK', 'Europe/London', 'Asia/Bangkok')"
            ))
            session.commit()
        
        client = TestClient(app)
        response = client.get("/flights")
        
        # expect success
        assert response.status_code == 200
        
        flights = response.json()["flights"]
        lhr_flight = next((f for f in flights if f["id"] == "LHR99"), None)
        
        assert lhr_flight is not None
        assert lhr_flight["departure_airport"] == "LHR"
        assert lhr_flight["arrival_airport"] == "BKK"
        
        departure_time = lhr_flight["departure_time"]
        arrival_time = lhr_flight["arrival_time"]
        
        # expect flight details with correct timezone conversion
        assert departure_time == "2024-12-15T10:00:00Z"
        assert arrival_time == "2024-12-16T01:00:00+07:00"
        

    def test_retrieve_flight_with_same_timezone(self, override_db):
        with override_db.session() as session:
            session.execute(text(
                "INSERT INTO flights (id, departure_time, arrival_time, departure_airport, arrival_airport, departure_timezone, arrival_timezone) "
                "VALUES ('BKK99', '2024-12-20T08:00:00Z', '2024-12-20T10:30:00Z', 'BKK', 'CNX', 'Asia/Bangkok', 'Asia/Bangkok')"
            ))
            session.commit()
        
        client = TestClient(app)
        response = client.get("/flights")
        
        assert response.status_code == 200
        
        flights = response.json()["flights"]
        bkk_flight = next((f for f in flights if f["id"] == "BKK99"), None)
        
        assert bkk_flight is not None
        assert bkk_flight["departure_airport"] == "BKK"
        assert bkk_flight["arrival_airport"] == "CNX"
        
        departure_time = bkk_flight["departure_time"]
        arrival_time = bkk_flight["arrival_time"]
        
        # expect flight details with same timezone
        assert departure_time == "2024-12-20T15:00:00+07:00"
        assert arrival_time == "2024-12-20T17:30:00+07:00"