from fastapi import APIRouter
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO
from src.infrastructure.user_repository_postgresql import UserTable
from src.infrastructure.firebase import sign_up as firebase_sign_up
user_routes = APIRouter(prefix="/user")
user_repository = UserTable()

#Transaction Model
def requests_user_with_id(id: str):
    return user_repository.find_by_id(id)

def wants_to_create_user(user_data: UserSignUpDTO):
    firebase_sign_up(user_data.email, user_data.password)
    user_repository.create(user_data)

def wants_to_delete_user(user_data: UserDTO):
    raise NotImplementedError

def wants_to_subscribe_to_training(training_id: int):
    raise NotImplementedError

#@user_routes.get("/")
# async def users():
#     session = SessionLocal()
#     return session.query(UserModel).all()
    
# @user_routes.delete("/{id}")
# async def delete_user(id: str):
#     session = SessionLocal()
#     user_to_delete = session.query(UserModel).filter(UserModel.id == id).first()
#     session.delete(user_to_delete)
#     session.commit()