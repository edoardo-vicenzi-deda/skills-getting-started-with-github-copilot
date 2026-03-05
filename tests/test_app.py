from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    # Arrange
    endpoint = "/"

    # Act
    response = client.get(endpoint, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_payload(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "Chess Club" in body
    assert "participants" in body["Chess Club"]


def test_signup_existing_activity_succeeds(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = quote("Unknown Club", safe="")
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_existing_participant_succeeds(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = quote("Unknown Club", safe="")
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_non_enrolled_email_returns_404(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "not.enrolled@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
