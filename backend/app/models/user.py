from sqlalchemy import Column, String, Integer
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique = True)
    role = Column(String, default = "client")
    hashed_password = Column(String)
    role = Column(String, default="moderator")  # moderator | admin
    is_active = Column(Boolean, default=True)
