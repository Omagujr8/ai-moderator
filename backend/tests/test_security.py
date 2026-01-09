def test_moderation_requires_api_key(client):
    response = client.post(
        "/api/v1/moderation/analyse",
        json={"text": "hello world"}
    )

    assert response.status_code in (401, 403)
