from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from src.infrastructure.database import Base, engine


class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    firstname = Column(String)

Base.metadata.create_all(bind=engine)