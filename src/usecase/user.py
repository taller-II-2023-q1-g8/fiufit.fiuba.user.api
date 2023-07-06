"""Application Service for Users"""
import datetime
from fastapi import exceptions
from src.domain.user.block_repository import IBlockRepository
from src.domain.user.follow_repository import IFollowRepository
from src.domain.user.user_repository import IUserRepository
from src.infrastructure.models.coordinates import Coordinates
from src.infrastructure.models.user_dto import UpdateUserDTO, UserDTO, UserSignUpDTO


class UserService:
    """Application Service for Users Definition"""

    FOLLOWER_MILESTONES = [10, 50, 100]

    def __init__(
        self,
        user_repository: IUserRepository,
        auth_service,
        notification_service,
        follow_repository: IFollowRepository,
        block_repository: IBlockRepository,
    ):
        self.user_repository = user_repository
        self.auth_service = auth_service
        self.notification_service = notification_service
        self.follow_repository = follow_repository
        self.block_repository = block_repository

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
# FALTA
    def wants_to_follow_user(self, follower_username: str, followed_username: str):
        """User wants to follow a user"""
        self.follow_repository.create(follower_username, followed_username)

        new_follower_count = len(
            self.follow_repository.find_by_following_username(followed_username)
        )

        if new_follower_count in self.FOLLOWER_MILESTONES:
            device_token = self.requests_device_token_for_user(followed_username)
            title = "Hito de Seguidores Alcanzado!"
            body = f"Haz alcanzado los {new_follower_count} seguidores"

            self.notification_service.send_notification(device_token, title, body)
# FALTA
    def wants_to_unfollow_user(self, follower_username: str, followed_username: str):
        """User wants to unfollow a user"""
        follow = self.follow_repository.find_by_pair(
            follower_username, followed_username
        )
        if follow is not None:
            self.follow_repository.remove(follow)

    def wants_to_delete_user(self, username: str):
        """User wants to delete a user"""
        try:
            self.user_repository.delete(username)
        except Exception as exc:
            raise exceptions.HTTPException(
                status_code=404, detail="user to delete not found"
            ) from exc

    def wants_to_update_user(self, user_data: UpdateUserDTO):
        """User wants to update an user"""
        # try:
        self.user_repository.update(user_data)
        # except Exception as exc:
        #     raise exceptions.HTTPException(
        #         status_code=404, detail="user to update not found"
        #     ) from exc
# FALTA
    def requests_followed_users(self, username: str):
        """User requests followed users"""
        results = self.follow_repository.find_by_follower_username(username)
        return list(map(lambda follow: follow.followed_username, results))
# FALTA
    def requests_follower_users(self, username: str):
        """User requests follower users"""
        results = self.follow_repository.find_by_following_username(username)
        return list(map(lambda follow: follow.follower_username, results))

    def wants_to_update_device_token(self, username: str, device_token: str):
        """User wants to update device token"""
        if username not in self.user_repository.all_non_admin_usernames():
            raise exceptions.HTTPException(status_code=404, detail="User not found")
        
        user_with_token = self.user_repository.find_by_device_token(device_token)
        if user_with_token is not None:
            self.user_repository.remove_user_device_token(user_with_token.username)

        self.user_repository.update_device_token(username, device_token)

    def wants_to_update_last_login(self, username: str):
        """User wants to update last login time"""
        self.user_repository.update_user_last_login(username)

    def requests_device_token_for_user(self, username: str):
        """User requests a user's device token"""
        if username not in self.user_repository.all_non_admin_usernames():
            raise exceptions.HTTPException(status_code=404, detail="User not found")

        token = self.user_repository.get_device_token(username)
        if token is None:
            raise exceptions.HTTPException(status_code=404, detail="Token not found")
        return token.device_token
# FALTA
    def asks_if_user_is_blocked(self, username: str):
        """User asks if a user is blocked"""
        if username not in self.user_repository.all_non_admin_usernames():
            raise exceptions.HTTPException(status_code=404, detail="User not found")

        block = self.block_repository.find_by_blocked_username(username)

        if block is None:
            return {"blocked": False}
        else:
            return {
                "blocked": True,
                "blocked_user": block.blocked_user,
                "blocked_by": block.blocked_by,
                "when": block.created_at,
            }
# FALTA
    def wants_to_block_user(self, user_to_block: str, admin_username: str):
        """Wants to block a user"""

        if admin_username not in self.user_repository.all_admin_usernames():
            raise exceptions.HTTPException(
                status_code=403, detail="You don't have enough permissions"
            )

        if user_to_block not in self.user_repository.all_non_admin_usernames():
            raise exceptions.HTTPException(status_code=404, detail="User not found")

        if self.block_repository.find_by_blocked_username(user_to_block) is None:
            self.block_repository.create(user_to_block, admin_username)
# FALTA
    def wants_to_unblock_user(self, user_to_unblock: str):
        """Wants to unblock a user"""
        block = self.block_repository.find_by_blocked_username(user_to_unblock)
        if block:
            self.block_repository.remove(user_to_unblock)

    def wants_to_increment_password_changes(self, username: str):
        """Wants to increment password changes"""
        self.user_repository.increment_password_changes(username)

    def wants_to_update_coordinates(self, username: str, coordinates: Coordinates):
        """Wants to update coordinates for username"""
        self.user_repository.update_coordinates(username, coordinates)
