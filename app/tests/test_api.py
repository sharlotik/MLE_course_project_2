from fastapi.testclient import TestClient
from models.event import Event

def test_home_request(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    
def test_get_events(client: TestClient):
    response = client.get("/api/events/")
    assert response.status_code == 200
    assert response.json() == []
    
def test_create_event(client: TestClient):
    event_data = {
        "id": 1,
        "title": "title",
        "image": "img",
        "description": "description",
       "creator_id": 1, 
        "status": "Success",
        "prediction":"Kolibri"
    }
    
    response = client.post("/api/events/new/", json=event_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Event created successfully"}

 
def test_get_event(client: TestClient):
    event_data = {
        "id": 1,
        "title": "title",
        "image": "img",
        "description": "description",
        "creator_id": 1, 
        "status": "Success",
        "prediction":"Kolibri"
    }
    
    response = client.get("/api/events/1/")
    
    print(response.json())
    
    assert response.status_code == 200
    assert response.json() == event_data

def test_clear_events(client: TestClient):
    response = client.delete("/api/events/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Events deleted successfully"}
 

def test_delete_event(client: TestClient):
    response = client.get("/api/events/")
    
    assert response.status_code == 200
    assert response.json() == []