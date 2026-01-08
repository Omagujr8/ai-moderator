from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Content(Base):
    __tablename__ = 'content'

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, index=True)
    text = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    username_hashed = Column(String, index=True)
    content_type = Column(String, index=True)
    source_app = Column(String, index=True)

    status = Column(String, default='pending')

    create_at = Column(DateTime(timezone=True), server_default=func.now())

    