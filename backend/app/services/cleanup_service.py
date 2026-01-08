from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.content import Content
from app.core.database import SessionLocal
from app.core.config import DELETE_AFTER_DAYS
import logging

logger = logging.getLogger("moderator_cleanup")

def cleanup_old_content():
    db: Session = SessionLocal()
    cutoff_date = datetime.utcnow() - timedelta(days=DELETE_AFTER_DAYS)
    old_contents = db.query(Content).filter(Content.created_at < cutoff_date).all()

    for content in old_contents:
        logger.info(f"Deleting content id = {content.id} created at {content.created_at}")
        db.delete(content)

    db.commit()
    db.close()
