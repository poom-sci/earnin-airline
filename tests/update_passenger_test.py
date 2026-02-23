import pytest
from fastapi.testclient import TestClient

from earnin_airline.app import app

class TestUpdatePassenger:
    
    def test_update_customer_information_and_flight_details(self, override_db):
        flight_id = "AAA01"
        
        initial_booking = {
            "passport_id": "BC1500",
            "first_name": "Shauna",
            "last_name": "Davila",
        }
        
        client = TestClient(app)
        create_response = client.post(
            f"/flights/{flight_id}/passengers",
            json=initial_booking,
        )
        
        assert create_response.status_code == 200
        customer_id = create_response.json()["customer_id"]
        
        updated_booking = {
            "passport_id": "BC1501",
            "first_name": "John",
            "last_name": "Doe",
        }
        
        update_response = client.put(
            f"/flights/{flight_id}/passengers/{customer_id}",
            json=updated_booking,
        )
        
        print(f"Update response status: {update_response.status_code}")
        print(f"Update response body: {update_response.json()}")
        
        assert update_response.status_code == 200
        
        response_data = update_response.json()
        assert response_data["customer_id"] == customer_id
        assert response_data["flight_id"] == flight_id
        assert response_data["passport_id"] == updated_booking["passport_id"]
        assert response_data["first_name"] == updated_booking["first_name"]
        assert response_data["last_name"] == updated_booking["last_name"]
        
        list_response = client.get(f"/flights/{flight_id}/passengers")
        passengers = list_response.json()["passengers"]
        
        # updated_passenger = next((p for p in passengers if p["customer_id"] == customer_id), None)
        
        assert passengers[0] is not None
        assert passengers[0]["passport_id"] == updated_booking["passport_id"]
        assert passengers[0]["first_name"] == updated_booking["first_name"]
        assert passengers[0]["last_name"] == updated_booking["last_name"]
    
    
    def test_update_customer_with_mismatched_name(self, override_db):
        flight_id = "AAA01"
        
        initial_booking = {
            "passport_id": "BC1500",
            "first_name": "Shauna",
            "last_name": "Davila",
        }
        
        client = TestClient(app)
        create_response = client.post(
            f"/flights/{flight_id}/passengers",
            json=initial_booking,
        )
        
        assert create_response.status_code == 200
        customer_id = create_response.json()["customer_id"]
        
        mismatched_booking = {
            "passport_id": "BC1501",
            "first_name": "Wrong",
            "last_name": "Name",
        }
        
        update_response = client.put(
            f"/flights/{flight_id}/passengers/{customer_id}",
            json=mismatched_booking,
        )
        
        assert update_response.status_code == 400
        
        response_data = update_response.json()
        assert "Firstname or Lastname is mismatch" in response_data["detail"]
        
        list_response = client.get(f"/flights/{flight_id}/passengers")
        passengers = list_response.json()["passengers"]

        assert passengers[0] is not None
        assert passengers[0]["passport_id"] == initial_booking["passport_id"]
        assert passengers[0]["first_name"] == initial_booking["first_name"]
        assert passengers[0]["last_name"] == initial_booking["last_name"]