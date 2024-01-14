from sqlalchemy import String, Integer, Column, Boolean, text, TIMESTAMP
from .database import Base

class Post(Base):
    __tablename__ = "posts"


    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    rating = Column(Integer, server_default=text('0'),nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)