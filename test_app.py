from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_activities_endpoint_returns_data():
    response = client.get("/activities")
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload


def test_signup_duplicate_is_rejected():
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_them_from_activity():
    response = client.delete("/activities/Chess%20Club/unregister?email=daniel@mergington.edu")
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"

    updated = client.get("/activities")
    assert "daniel@mergington.edu" not in updated.json()["Chess Club"]["participants"]
