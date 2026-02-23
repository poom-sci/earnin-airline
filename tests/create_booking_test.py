import pytest
from fastapi.testclient import TestClient

from earnin_airline.app import app

class TestCreateBookingIntegration:
    
    def test_create_booking_with_valid_customer_and_flight_details(self, override_db):
        flight_id = "AAA01"        
        booking_request = {
            "passport_id": "BC1500",
            "first_name": "Shauna",
            "last_name": "Davila",
        }
        
        client = TestClient(app)
        response = client.post(
            f"/flights/{flight_id}/passengers",
            json=booking_request,
        )
    
        # check if 200 ok
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["flight_id"] == flight_id
        assert response_data["passport_id"] == booking_request["passport_id"]
        assert response_data["first_name"] == booking_request["first_name"]
        assert response_data["last_name"] == booking_request["last_name"]
        assert "customer_id" in response_data
        assert response_data["customer_id"] >= 1
        


class TestCreateBookingMismatchName:
    
    def test_create_booking_with_mismatched_customer_name(self, override_db):
        flight_id = "AAA01"
        
        booking_request = {
            "passport_id": "BC1500",
            "first_name": "John",
            "last_name": "Doe",
        }
        
        client = TestClient(app)
        response = client.post(
            f"/flights/{flight_id}/passengers",
            json=booking_request,
        )
        
        assert response.status_code == 400
        
        response_data = response.json()
        assert "Firstname or Lastname is mismatch" in response_data["detail"]
        