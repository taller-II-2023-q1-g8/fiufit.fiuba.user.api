from fastapi import APIRouter
from ddd.infrastructure.database import SessionLocal
from ddd.infrastructure.models import UserModel
from ddd.infrastructure.user_dto import UserDTO

user_routes = APIRouter(prefix="/user")

@user_routes.get("/")
async def users():
    session = SessionLocal()
    return session.query(UserModel).all()

@user_routes.get("/{id}")
async def user_with_id(id: str):
    session = SessionLocal()
    return session.query(UserModel).filter(UserModel.id == id).first()

@user_routes.put("/")
async def create_user(data: UserDTO):
    session = SessionLocal()
    session.add(UserModel(id=data.id, firstname=data.firstname))
    session.commit()
    
@user_routes.delete("/{id}")
async def delete_user(id: str):
    session = SessionLocal()
    user_to_delete = session.query(UserModel).filter(UserModel.id == id).first()
    session.delete(user_to_delete)
    session.commit()

