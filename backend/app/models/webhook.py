from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True)
    source_app = Column(String, unique=True)
    callback_url = Column(String)
