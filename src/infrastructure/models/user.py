"""User Model for ORM"""
from sqlalchemy import Column, String, Date, Numeric, Boolean
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
    lastname = Column(String)
    weight_in_kg = Column(Numeric(5, 2))
    height_in_cm = Column(Numeric(4, 1))
    is_federated = Column(Boolean)


Base.metadata.create_all(bind=engine)
