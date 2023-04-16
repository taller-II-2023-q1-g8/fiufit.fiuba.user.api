"""Application Service for Users"""
from fastapi import exceptions
from src.domain.user.user_repository import IUserRepository
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO


class UserService():
    """Application Service for Users Definition"""
    def __init__(self, user_repository: IUserRepository, auth_service):
        self.user_repository = user_repository
        self.auth_service = auth_service

    #Transaction Model
    def requests_all_usernames(self):
        """User requests all usernames"""
        return self.user_repository.all_usernames()

    def requests_user_with_username(self, username: str):
        """User requests user with username"""
        return self.user_repository.find_by_username(username)

    def wants_to_create_user(self, user_data: UserSignUpDTO):
        """User wants to create a new user"""
        try:
            self.user_repository.create(user_data=user_data)
        except Exception as exc:
            if self.user_repository.find_by_email(user_data.email) is not None:
                raise exceptions.HTTPException(status_code=409,
                    detail="Email already exists") from exc
            else:
                raise exceptions.HTTPException(status_code=409,
                    detail="Username already exists") from exc
        else:
            try:
                self.auth_service.sign_up(user_data.email, user_data.password)
            except Exception as exc:
                self.user_repository.delete(user_data.username)
                raise exceptions.HTTPException(status_code=500,
                    detail="Firebase Error") from exc

    def wants_to_delete_user(self, username: str):
        """User wants to delete a user"""
        try:
            self.user_repository.delete(username)
        except Exception as exc:
            raise exceptions.HTTPException(status_code=404,
                detail="user to delete not found") from exc

    def wants_to_update_user(self, user_data: UserDTO):
        """User wants to update an user"""
        try:
            self.user_repository.update(user_data)
        except Exception as exc:
            raise exceptions.HTTPException(status_code=404,
                detail="user to update not found") from exc

    def wants_to_subscribe_to_training(self, training_id: int):
        """User wants to subscribe to a training"""
        raise NotImplementedError
