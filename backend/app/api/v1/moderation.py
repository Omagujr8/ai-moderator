from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.content import ContentCreate, ContentResponse
from app.models.content import Content
from app.core.database import get_db
from app.workers.moderation_worker import moderate_content_task
from app.core.security import verify_api_key
from app.core.rate_limit import limiter

router = APIRouter(prefix="/moderation", tags=["Moderation"])


@router.post(
    "/analyse",
    response_model=ContentResponse,
    dependencies=[Depends(verify_api_key)]
)
@limiter.limit("30/minute")
def analyse_content(
    request: Request,
    payload: ContentCreate,
    db: Session = Depends(get_db)
):
    content = Content(**payload.dict())
    db.add(content)
    db.commit()
    db.refresh(content)

    moderate_content_task.delay(content.id)

    return content
