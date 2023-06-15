"""Application Service for Users"""
import datetime
from fastapi import exceptions
from src.domain.user.user_repository import IUserRepository
from src.infrastructure.models.blocked_user import BlockedUserModel
from src.infrastructure.models.follow import FollowModel
from src.infrastructure.models.user import UserModel
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO
from src.infrastructure.models.user_device import UserDeviceToken
from src.infrastructure.database import SessionLocal


class UserService:
    """Application Service for Users Definition"""

    def __init__(self, user_repository: IUserRepository, auth_service):
        self.user_repository = user_repository
        self.auth_service = auth_service

    # Transaction Model
    def requests_all_non_admin_users(self):
        """User requests all non-admin users"""
        return self.user_repository.all_non_admin()

    def requests_all_admin_users(self):
        """User requests all admin users"""
        return self.user_repository.all_admins()

    def requests_all_non_admin_usernames(self):
        """User requests all non-admin usernames"""
        return self.user_repository.all_non_admin_usernames()

    def requests_all_admin_usernames(self):
        """User requests all admin usernames"""
        return self.user_repository.all_admin_usernames()

    def requests_non_admin_usernames_starting_with(self, prefix: str):
        """User requests non-admin usernames starting with"""
        return self.user_repository.non_admin_usernames_starting_with(prefix=prefix)

    def requests_admin_usernames_starting_with(self, prefix: str):
        """User requests admin usernames starting with"""
        return self.user_repository.admin_usernames_starting_with(prefix=prefix)

    def requests_non_admin_user_with_username(self, username: str):
        """User requests user with username"""
        return self.user_repository.find_non_admin_by_username(username)

    def requests_non_admin_user_with_email(self, email: str):
        """User requests user with email"""
        return self.user_repository.find_non_admin_by_email(email)

    def requests_admin_user_with_username(self, username: str):
        """User requests user with username"""
        return self.user_repository.find_admin_by_username(username)

    def requests_admin_user_with_email(self, email: str):
        """User requests user with email"""
        return self.user_repository.find_admin_by_email(email)

    def wants_to_create_user(self, user_data: UserSignUpDTO):
        """User wants to create a new user"""
        try:
            self.user_repository.create(user_data=user_data)
        except Exception as exc:
            admin = self.user_repository.find_admin_by_email(user_data.email)
            non_admin = self.user_repository.find_non_admin_by_email(user_data.email)
            if admin is not None or non_admin is not None:
                raise exceptions.HTTPException(
                    status_code=409, detail="Email already exists"
                ) from exc
            else:
                raise exceptions.HTTPException(
                    status_code=409, detail="Username already exists"
                ) from exc
        if not user_data.is_federated:
            try:
                self.auth_service.sign_up(user_data.email, user_data.password)
            except Exception as exc:
                self.user_repository.delete(user_data.username)
                raise exceptions.HTTPException(
                    status_code=500, detail="Firebase Error"
                ) from exc

    def wants_to_follow_user(self, follower_username: str, followed_username: str):
        session = SessionLocal()
        follower = self.user_repository.find_non_admin_by_username(follower_username)
        followed = self.user_repository.find_non_admin_by_username(followed_username)

        if (follower is not None) and (followed is not None):
            if (
                session.query(FollowModel)
                .filter(FollowModel.followed_username == followed_username)
                .filter(FollowModel.follower_username == follower_username)
                .first()
                is None
            ):
                session.add(
                    FollowModel(
                        follower_username=follower_username,
                        followed_username=followed_username,
                    )
                )
                session.commit()

    def wants_to_unfollow_user(self, follower_username: str, followed_username: str):
        session = SessionLocal()

        follow_to_delete = (
            session.query(FollowModel)
            .filter(FollowModel.followed_username == followed_username)
            .filter(FollowModel.follower_username == follower_username)
            .first()
        )

        session.delete(follow_to_delete)
        session.commit()

    def wants_to_delete_user(self, username: str):
        """User wants to delete a user"""
        try:
            self.user_repository.delete(username)
        except Exception as exc:
            raise exceptions.HTTPException(
                status_code=404, detail="user to delete not found"
            ) from exc

    def wants_to_update_user(self, user_data: UserDTO):
        """User wants to update an user"""
        try:
            self.user_repository.update(user_data)
        except Exception as exc:
            raise exceptions.HTTPException(
                status_code=404, detail="user to update not found"
            ) from exc

    def wants_to_subscribe_to_training(self, training_id: int):
        """User wants to subscribe to a training"""
        raise NotImplementedError

    def requests_followed_users(self, username: str):
        """User requests followed users"""
        session = SessionLocal()
        query_resuls = (
            session.query(FollowModel)
            .filter(FollowModel.follower_username == username)
            .all()
        )

        return list(map(lambda follow: follow.followed_username, query_resuls))

    def requests_follower_users(self, username: str):
        """User requests follower users"""
        session = SessionLocal()
        query_resuls = (
            session.query(FollowModel)
            .filter(FollowModel.followed_username == username)
            .all()
        )

        return list(map(lambda follow: follow.follower_username, query_resuls))

    def wants_to_update_device_token(self, username: str, device_token: str):
        """User wants to update device token"""
        if username not in self.user_repository.all_non_admin_usernames():
            raise exceptions.HTTPException(status_code=404, detail="User not found")

        session = SessionLocal()
        table_entry = (
            session.query(UserDeviceToken)
            .filter(UserDeviceToken.username == username)
            .first()
        )
        if table_entry is None:
            print("Is None")
            table_entry = UserDeviceToken()
            table_entry.username = username
            table_entry.device_token = device_token
            session.add(table_entry)
            print(table_entry.device_token)
        else:
            print("Isn't None")
            table_entry.device_token = device_token
            print(table_entry.device_token)
        session.commit()

    def wants_to_update_last_login(self, username: str):
        """User wants to update last login time"""
        if username not in self.user_repository.all_non_admin_usernames():
            raise exceptions.HTTPException(status_code=404, detail="User not found")

        session = SessionLocal()
        table_entry = (
            session.query(UserModel).filter(UserModel.username == username).first()
        )
        table_entry.last_login = datetime.datetime.now()
        session.commit()

    def requests_device_token_for_user(self, username: str):
        """User requests a user's device token"""
        if username not in self.user_repository.all_non_admin_usernames():
            raise exceptions.HTTPException(status_code=404, detail="User not found")

        session = SessionLocal()
        table_entry = (
            session.query(UserDeviceToken)
            .filter(UserDeviceToken.username == username)
            .first()
        )
        if table_entry is None:
            raise exceptions.HTTPException(status_code=404, detail="Token not found")

        return table_entry.device_token

    def asks_if_user_is_blocked(self, username: str):
        """User asks if a user is blocked"""
        if username not in self.user_repository.all_non_admin_usernames():
            raise exceptions.HTTPException(status_code=404, detail="User not found")

        session = SessionLocal()
        table_entry = (
            session.query(BlockedUserModel)
            .filter(BlockedUserModel.blocked_user == username)
            .first()
        )

        if table_entry is None:
            return {"blocked": False}
        else:
            return {
                "blocked": True,
                "blocked_user": table_entry.blocked_user,
                "blocked_by": table_entry.blocked_by,
                "when": table_entry.created_at,
            }

    def wants_to_block_user(self, user_to_block: str, admin_username: str):
        """Wants to block a user"""

        if admin_username not in self.user_repository.all_admin_usernames():
            raise exceptions.HTTPException(
                status_code=403, detail="You don't have enough permissions"
            )

        if user_to_block not in self.user_repository.all_non_admin_usernames():
            raise exceptions.HTTPException(status_code=404, detail="User not found")

        session = SessionLocal()
        table_entry = (
            session.query(BlockedUserModel)
            .filter(BlockedUserModel.blocked_user == user_to_block)
            .first()
        )

        if table_entry is None:
            table_entry = BlockedUserModel()
            table_entry.blocked_user = user_to_block
            table_entry.blocked_by = admin_username
            table_entry.created_at = datetime.datetime.now()
            session.add(table_entry)
            session.commit()

    def wants_to_unblock_user(self, user_to_unblock: str):
        """Wants to unblock a user"""

        session = SessionLocal()
        table_entry = (
            session.query(BlockedUserModel)
            .filter(BlockedUserModel.blocked_user == user_to_unblock)
            .first()
        )

        if table_entry is not None:
            session.delete(table_entry)
            session.commit()

    def wants_to_increment_password_changes(self, username: str):
        """Wants to increment password changes"""
        session = SessionLocal()
        table_entry = (
            session.query(UserModel).filter(UserModel.username == username).first()
        )
        if table_entry is None:
            raise exceptions.HTTPException(status_code=404, detail="User not found")
        
        table_entry.password_changes += 1
        session.commit()