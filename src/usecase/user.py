from fastapi import APIRouter, status, exceptions
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO
from src.infrastructure.firebase import sign_up as firebase_sign_up

class UserService():
    def __init__(self, user_repository):
        self.user_repository = user_repository    

    #Transaction Model
    def requests_user_with_id(self, id: str):
        return self.user_repository.find_by_id(id)

    def wants_to_create_user(self, user_data: UserSignUpDTO):
        try:
            firebase_sign_up(user_data.email, user_data.password)
        except:
            raise exceptions.HTTPException(status_code=406, detail="email already exists")
        try:
            self.user_repository.create(user_data)
        except:
            raise exceptions.HTTPException(status_code=406, detail="id already exists")

    def wants_to_delete_user(self, user_data: UserDTO):
        raise NotImplementedError

    def wants_to_subscribe_to_training(self, training_id: int):
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