from fastapi import APIRouter
from ddd.infrastructure.user_dto import UserDTO
from ddd.infrastructure.user_repository_postgresql import UserTable

user_routes = APIRouter(prefix="/user")
user_repository = UserTable()

#Transaction Model
@user_routes.get("/{id}")
async def requests_user_with_id(id: str):
    return user_repository.find_by_id(id)

@user_routes.put("/")
async def wants_to_create_user(user_data: UserDTO):
    user_repository.create(user_data)

@user_routes.delete("/{id}")
async def wants_to_delete_user(user_data: UserDTO):
    raise NotImplementedError

@user_routes.post("/subscribe-to-training")
async def wants_to_subscribe_to_training(training_id: int):
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