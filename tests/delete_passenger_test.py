import pytest
from fastapi.testclient import TestClient

from earnin_airline.app import app

class TestDeletePassenger:
    
    def test_delete_valid_booking(self, override_db):
        flight_id = "AAA01"
        
        booking_request = {
            "passport_id": "BC1500",
            "first_name": "Shauna",
            "last_name": "Davila",
        }
        
        
        client = TestClient(app)
        create_response = client.post(
            f"/flights/{flight_id}/passengers",
            json=booking_request,
        )
        
        assert create_response.status_code == 200
        customer_id = create_response.json()["customer_id"]
        
        delete_response = client.delete(
            f"/flights/{flight_id}/passengers/{customer_id}"
        )
        
        assert delete_response.status_code == 200
        
        list_response = client.get(f"/flights/{flight_id}/passengers")
        passengers = list_response.json()["passengers"]
        
        assert len(passengers) == 0