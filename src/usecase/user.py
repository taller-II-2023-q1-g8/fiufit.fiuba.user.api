"""Application Service for Users"""
from fastapi import exceptions
from src.domain.user.user_repository import IUserRepository
from src.infrastructure.models.follow import FollowModel
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO
from src.infrastructure.database import SessionLocal


class UserService():
    """Application Service for Users Definition"""
    def __init__(self, user_repository: IUserRepository, auth_service):
        self.user_repository = user_repository
        self.auth_service = auth_service

    #Transaction Model
    def requests_all_users(self):
        """User requests all users"""
        return self.user_repository.all()

    def requests_all_usernames(self):
        """User requests all usernames"""
        return self.user_repository.all_usernames()

    def requests_usernames_starting_with(self, prefix: str):
        """User requests usernames starting with"""
        return self.user_repository.usernames_starting_with(prefix=prefix)

    def requests_user_with_username(self, username: str):
        """User requests user with username"""
        return self.user_repository.find_by_username(username)

    def requests_user_with_email(self, email: str):
        """User requests user with email"""
        return self.user_repository.find_by_email(email)

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
        if not user_data.is_federated:
            try:
                self.auth_service.sign_up(user_data.email, user_data.password)
            except Exception as exc:
                self.user_repository.delete(user_data.username)
                raise exceptions.HTTPException(status_code=500,
                    detail="Firebase Error") from exc
            
    def wants_to_follow_user(self, follower_username: str, followed_username: str):
        session = SessionLocal()
        follower = self.user_repository.find_by_username(follower_username)
        followed = self.user_repository.find_by_username(followed_username)
        
        if (follower is not None) and (followed is not None):
            if session.query(FollowModel)\
                .filter(FollowModel.followed_username == followed_username)\
                .filter(FollowModel.follower_username == follower_username).first() is None:
                session.add(FollowModel(
                    follower_username=follower_username,
                    followed_username=followed_username))
                session.commit()

    def wants_to_unfollow_user(self, follower_username: str, followed_username: str):
        session = SessionLocal()

        follow_to_delete = session.query(FollowModel)\
            .filter(FollowModel.followed_username == followed_username)\
            .filter(FollowModel.follower_username == follower_username).first()
        
        session.delete(follow_to_delete)
        session.commit()

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

    def requests_followed_users(self, username: str):
        """User requests followed users"""
        session = SessionLocal()
        query_resuls = session.query(FollowModel)\
            .filter(FollowModel.follower_username == username).all()
        
        return list(map(lambda follow: follow.followed_username, query_resuls))

    def requests_follower_users(self, username: str):
        """User requests follower users"""
        session = SessionLocal()
        query_resuls = session.query(FollowModel) \
            .filter(FollowModel.followed_username == username).all()

        return list(map(lambda follow: follow.follower_username, query_resuls))