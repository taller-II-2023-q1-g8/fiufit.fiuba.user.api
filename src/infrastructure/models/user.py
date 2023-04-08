from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
from src.infrastructure.database import Base, engine


class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String)
    phone_number = Column(String)
    gender = Column(String)
    birth_date = Column(Date)
    firstname = Column(String)

Base.metadata.create_all(bind=engine)