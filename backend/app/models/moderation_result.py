from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class ModerationResult(Base):
    __tablename__ = "moderation_result"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"))
    category = Column(String, index=True)
    score = Column(Float)
    decision = Column(String)
    model_version = Column(String)

    created_at = Column(DateTime(timezone = True), server_default=func.now())
