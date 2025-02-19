from src.infrastructure.database import Base, engine
from sqlalchemy import Column, String, ForeignKey

class UserDeviceToken(Base):
    __tablename__ = "devices_tokens"
    username = Column(String, ForeignKey("users.username"), primary_key=True)
    device_token = Column(String, unique=True)

if Base is not None and engine is not None:
    Base.metadata.create_all(bind=engine)