def test_root_health(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Ok", "Service": "AI Content Moderator"}