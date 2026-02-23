import pytest
from tests.conftest import create_passenger

TEST_FLIGHT_ID = "AAA01"

class TestDeletePassenger:
    
    def test_delete_valid_booking(self, client, override_db):
        create_resp = create_passenger(client, TEST_FLIGHT_ID, "BC1500", "Shauna", "Davila")
        customer_id = create_resp.json()["customer_id"]
        
        delete_resp = client.delete(f"/flights/{TEST_FLIGHT_ID}/passengers/{customer_id}")
        # expect success
        assert delete_resp.status_code == 200
        
        list_resp = client.get(f"/flights/{TEST_FLIGHT_ID}/passengers")
        passengers = list_resp.json()["passengers"]
        # expect no passengers after deletion
        assert len(passengers) == 0