from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.content import ContentCreate, ContentResponse
from app.models.content import Content
from app.core.database import get_db
from app.core.security import verify_api_key
from app.core.rate_limit import limiter

router = APIRouter(prefix="/moderation", tags=["Moderation"])


@router.post(
    "/analyse",
    response_model=ContentResponse,
    dependencies=[Depends(verify_api_key)]
)
@limiter.limit("30/minute")
async def analyse_content(
    request: Request,
    payload: ContentCreate,
    db: Session = Depends(get_db)
):
    content = Content(**payload.model_dump())
    db.add(content)
    db.commit()
    db.refresh(content)

    # Queue async moderation task (gracefully skip if Redis/Celery unavailable)
    try:
        from app.workers.moderation_worker import moderate_content_task
        moderate_content_task.delay(content.id)
    except Exception:
        # Redis/Celery connection errors are non-fatal in testing
        pass

    return content
