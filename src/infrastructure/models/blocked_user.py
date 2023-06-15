from sqlalchemy import Column, String, ForeignKey, DateTime
from src.infrastructure.database import Base, engine

class BlockedUserModel(Base):
    __tablename__ = "blocked_users"
    blocked_by = Column(String, ForeignKey("users.username"), primary_key=True)
    blocked_user =  Column(String, ForeignKey("users.username"), primary_key=True)
    created_at = Column(DateTime)

Base.metadata.create_all(bind=engine)