from fastapi import APIRouter, status, exceptions
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO

class UserService():
    def __init__(self, user_repository, auth_service):
        self.user_repository = user_repository    
        self.auth_service = auth_service

    #Transaction Model
    def requests_all_usernames(self):
        return self.user_repository.all_usernames()

    def requests_user_with_username(self, username: str):
        return self.user_repository.find_by_username(username)

    def wants_to_create_user(self, user_data: UserSignUpDTO):
        try:
            self.user_repository.create(user_data=user_data)
        except Exception as e:
            print(e)
            raise exceptions.HTTPException(status_code=406)
        else:
            try:
                self.auth_service.sign_up(user_data.email, user_data.password)
            except Exception as e:
                print(e)
                self.delete_user(user_data.username)
                raise exceptions.HTTPException(status_code=500, detail="Firebase Error")
    
    def wants_to_delete_user(self, username: str):
        try:
            self.user_repository.delete(username)
        except:
            raise exceptions.HTTPException(status_code=404, detail="user to delete not found")

    def wants_to_update_user(self, user_data: UserDTO):
        try:
            self.user_repository.update(user_data)
        except:
            raise exceptions.HTTPException(status_code=404, detail="user to update not found")

    def wants_to_subscribe_to_training(self, training_id: int):
        raise NotImplementedError