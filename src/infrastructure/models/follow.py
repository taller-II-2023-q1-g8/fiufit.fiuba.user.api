from sqlalchemy import Column, String, ForeignKey
from src.infrastructure.database import Base, engine

class FollowModel(Base):
    __tablename__ = "follows"
    follower_username =  Column(String, ForeignKey("users.username"), primary_key=True)
    followed_username =  Column(String, ForeignKey("users.username"), primary_key=True)

if Base is not None and engine is not None:
    Base.metadata.create_all(bind=engine)