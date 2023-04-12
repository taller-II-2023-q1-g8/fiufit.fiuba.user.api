from fastapi import APIRouter, status, exceptions
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO

class UserService():
    def __init__(self, user_repository):
        self.user_repository = user_repository    

    #Transaction Model
    def requests_all_user_ids(self):
        return self.user_repository.all_user_ids()

    def requests_user_with_id(self, id: str):
        return self.user_repository.find_by_id(id)

    def wants_to_create_user(self, user_data: UserSignUpDTO):
        try:
            self.user_repository.create(user_data)
        except:
            raise exceptions.HTTPException(status_code=406, detail="id already exists")
    
    def wants_to_delete_user(self, d: str):
        try:
            self.user_repository.delete(id)
        except:
            raise exceptions.HTTPException(status_code=404, detail="user to delete not found")

    def wants_to_update_user(self, user_data: UserDTO):
        try:
            self.user_repository.update(user_data)
        except:
            raise exceptions.HTTPException(status_code=404, detail="user to update not found")

    def wants_to_subscribe_to_training(self, training_id: int):
        raise NotImplementedError