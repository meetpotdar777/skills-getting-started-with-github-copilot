from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_activities_endpoint_returns_data():
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload


def test_signup_duplicate_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_them_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"

    updated = client.get("/activities")
    assert email not in updated.json()[activity_name]["participants"]
