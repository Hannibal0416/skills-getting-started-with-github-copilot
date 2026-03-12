"""
Test activities endpoints for FastAPI backend using pytest and AAA pattern.
"""

def test_get_activities(client):
    # Arrange: (No special setup needed)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure the student is not already signed up
    client.post(f"/activities/{activity}/signup", params={"email": email})  # Clean up if needed

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
