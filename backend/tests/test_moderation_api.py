def test_moderation_endpoint(client):
    """Test that moderation endpoint accepts POST with proper auth and returns 200."""
    response = client.post(
        "/api/v1/moderation/analyse",
        headers={"X-API-KEY": "test-key-123"},
        json={
            "external_id": "test-1",
            "text": "I hate you",
            "content_type": "comment",
            "source_app": "pytest"
        }
    )

    assert response.status_code == 200
