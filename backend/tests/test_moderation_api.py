from unittest.mock import patch

def test_moderation_endpoint(client):
    with patch("app.api.v1.moderation.moderate_content_task.delay") as mock_delay:
        mock_delay.return_value = None

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
