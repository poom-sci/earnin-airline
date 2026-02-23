import pytest
from tests.conftest import create_passenger

TEST_FLIGHT_ID = "AAA01"

def update_passenger(client, flight_id, customer_id, payload):
    response = client.put(
        f"/flights/{flight_id}/passengers/{customer_id}",
        json=payload,
    )
    return response

class TestUpdatePassenger:
    
    def test_update_customer_information_and_flight_details(self, client, override_db):
        create_resp = create_passenger(client, TEST_FLIGHT_ID, "BC1500", "Shauna", "Davila")
        customer_id = create_resp.json()["customer_id"]
        
        update_resp = update_passenger(client, TEST_FLIGHT_ID, customer_id, {
            "passport_id": "BC1501",
            "first_name": "John",
            "last_name": "Doe"
        })
        
        # expect success
        assert update_resp.status_code == 200
        data = update_resp.json()
        assert data["customer_id"] == customer_id
        assert data["passport_id"] == "BC1501"
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
    
    def test_update_customer_with_mismatched_name(self, client, override_db):
        create_resp = create_passenger(client, TEST_FLIGHT_ID, "BC1500", "Shauna", "Davila")
        customer_id = create_resp.json()["customer_id"]
        
        update_resp = update_passenger(client, TEST_FLIGHT_ID, customer_id, {
            "passport_id": "BC1501",
            "first_name": "Wrong",
            "last_name": "Name"
        })
        
        # expect 400 error due to name mismatch
        assert update_resp.status_code == 400
        assert "Firstname or Lastname is mismatch" in update_resp.json()["detail"]
        
        list_resp = client.get(f"/flights/{TEST_FLIGHT_ID}/passengers")
        passengers = list_resp.json()["passengers"]
        assert passengers[0]["passport_id"] == "BC1500"
        assert passengers[0]["first_name"] == "Shauna"