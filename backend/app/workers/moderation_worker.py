from app.core.celery import celery_app
from app.services.moderation_service import run_moderation

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5 , retry_kwargs = {"max_retries": 3})
def moderate_content_task(self, content_id: int):
    run_moderation(content_id)
