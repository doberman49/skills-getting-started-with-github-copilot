def test_root_redirects_to_activity_page(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_data_without_cache(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert "Chess Club" in response.json()


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    response = client.post("/activities/Unknown%20Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_without_changing_participants(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    participants_before = client.get("/activities").json()[activity]["participants"]

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"
    assert client.get("/activities").json()[activity]["participants"] == participants_before


def test_unregister_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    response = client.delete("/activities/Unknown%20Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_unregistered_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"