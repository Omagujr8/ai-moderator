from locust import HttpUser, task, between

class ModerateTestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def moderate_text(self):
        self.client.post(
            "/api/v1/moderation/analyse",
            headers={
                "X-API-KEY": "test-key-123"
            },
            json={
                "external_id": "load",
                "text": "You are stupid",
                "content_type": "comment",
                "source_app": "locust"
            }
        )
