"""User Model for ORM"""
from sqlalchemy import Column, String, Date
from src.infrastructure.database import Base, engine


class UserModel(Base):
    "User Model Definition"
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    email = Column(String, unique=True)
    phone_number = Column(String)
    gender = Column(String)
    birth_date = Column(Date)
    firstname = Column(String)

Base.metadata.create_all(bind=engine)
