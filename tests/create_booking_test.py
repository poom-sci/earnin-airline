import pytest
from tests.conftest import create_passenger

TEST_FLIGHT_ID = "AAA01"

class TestCreateBooking:
    
    def test_create_booking_with_valid_customer_and_flight_details(self, client, override_db):
        response = create_passenger(client, TEST_FLIGHT_ID, "BC1500", "Shauna", "Davila")
        
        assert response.status_code == 200
        data = response.json()
        assert data["flight_id"] == TEST_FLIGHT_ID
        assert data["passport_id"] == "BC1500"
        assert data["first_name"] == "Shauna"
        assert data["last_name"] == "Davila"
        assert data["customer_id"] >= 1
    
    def test_create_booking_with_mismatched_customer_name(self, client, override_db):
        response = create_passenger(client, TEST_FLIGHT_ID, "BC1500", "John", "Doe")
        
        assert response.status_code == 400
        assert "Firstname or Lastname is mismatch" in response.json()["detail"]
        