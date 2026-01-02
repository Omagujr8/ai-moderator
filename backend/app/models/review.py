from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, ForeignKey('content.id'))
    reviewer = Column(String)
    decision = Column(String)
    note = Column(String)
