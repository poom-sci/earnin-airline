import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy import text

from earnin_airline.app import app

class TestFlightTimezoneConversion:
    
    def test_retrieve_flight_with_different_timezones(self, override_db):
        with override_db.session() as session:
            session.execute(text(
                "INSERT INTO flights (id, departure_time, arrival_time, departure_airport, arrival_airport, departure_timezone, arrival_timezone) "
                "VALUES ('LHR99', '2024-12-15T10:00:00Z', '2024-12-15T18:00:00Z', 'LHR', 'BKK', 'Europe/London', 'Asia/Bangkok')"
            ))
            session.commit()
        
        client = TestClient(app)
        response = client.get("/flights")
        
        assert response.status_code == 200
        
        flights = response.json()["flights"]
        lhr_flight = next((f for f in flights if f["id"] == "LHR99"), None)
        
        assert lhr_flight is not None
        assert lhr_flight["departure_airport"] == "LHR"
        assert lhr_flight["arrival_airport"] == "BKK"
        
        departure_time = lhr_flight["departure_time"]
        arrival_time = lhr_flight["arrival_time"]
        
        assert "T" in departure_time
        assert "T" in arrival_time
        
        print(f"Departure time (London): {departure_time}")
        print(f"Arrival time (Bangkok): {arrival_time}")
