from sqlalchemy import Column, String, Integer
fro app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique = True)
    role = Column(String, default = "client")
