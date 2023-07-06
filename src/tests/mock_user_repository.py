from abc import abstractmethod
import datetime
from typing import Optional
from src.domain.user.user import User
from src.domain.user.user_repository import IUserRepository
from src.infrastructure.models.coordinates import Coordinates
from src.infrastructure.models.user import UserModel
from src.infrastructure.models.user_device import UserDeviceToken
from src.infrastructure.models.user_dto import UpdateUserDTO, UserDTO, UserSignUpDTO


class MockUserRepository(IUserRepository):
    def __init__(self, users, device_tokens):
        self.users = users
        self.device_tokens = device_tokens

    def create(self, user_data: UserSignUpDTO) -> None:
        """Create a new user"""
        self.users.append(
            UserModel(
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                password_changes=0,
                last_login=None,
                username=user_data.username,
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                email=user_data.email,
                phone_number=user_data.phone_number,
                gender=user_data.gender,
                birth_date=user_data.birth_date,
                is_federated=user_data.is_federated,
                weight_in_kg=user_data.weight_in_kg,
                height_in_cm=user_data.height_in_cm,
                is_admin=user_data.is_admin,
                interests=user_data.interests,
            )
        )

    def all_non_admin(self) -> list:
        """Get all non-admin users"""
        return list(filter(lambda user: user.is_admin == False, self.users))

    def all_admins(self) -> list:
        """Get all admin users"""
        return list(filter(lambda user: user.is_admin == True, self.users))

    def all_non_admin_usernames(self) -> list:
        """Get all non-admin usernames"""
        return list(map(lambda user: user.username, self.all_non_admin()))

    def all_admin_usernames(self) -> list:
        """Get all admin usernames"""
        return list(map(lambda user: user.username, self.all_admins()))

    def non_admin_usernames_starting_with(self, prefix: str) -> list:
        """Get non-admin usernames starting with"""
        return list(
            filter(
                lambda username: username.startswith(prefix),
                self.all_non_admin_usernames(),
            )
        )

    def admin_usernames_starting_with(self, prefix: str) -> list:
        """Get admin usernames starting with"""
        return list(
            filter(
                lambda username: username.startswith(prefix),
                self.all_admin_usernames(),
            )
        )

    def find_non_admin_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        filtered = list(filter(lambda user: user.email == email, self.all_non_admin()))
        return filtered[0] if len(filtered) > 0 else None

    def find_non_admin_by_username(self, username: str) -> Optional[User]:
        """Find a user by username"""
        filtered = list(filter(lambda user: user.username == username, self.all_non_admin()))
        return filtered[0] if len(filtered) > 0 else None

    def find_admin_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        filtered = list(filter(lambda user: user.email == email, self.all_admins()))
        return filtered[0] if len(filtered) > 0 else None

    def find_admin_by_username(self, username: str) -> Optional[User]:
        """Find a user by username"""
        filtered = list(filter(lambda user: user.username == username, self.all_admins()))
        return filtered[0] if len(filtered) > 0 else None

    def delete(self, username: str):
        """Delete a user by username"""
        for i in range(len(self.users)):
            if self.users[i].username == username:
                self.users.pop(i)
                return

    def update(self, user_data: UpdateUserDTO):
        """Update a user"""
        user_to_update = self.find_non_admin_by_username(user_data.username)
        if user_to_update is None:
            user_to_update = self.find_admin_by_username(user_data.username)
            if user_to_update is None:
                return
        
        print(user_to_update)
        self.users.remove(user_to_update)
        user_to_update.updated_at = datetime.datetime.now()
        user_to_update.username = user_data.username
        user_to_update.firstname = user_data.firstname
        user_to_update.lastname = user_data.lastname
        user_to_update.email = user_data.email
        user_to_update.phone_number = user_data.phone_number
        user_to_update.gender = user_data.gender
        user_to_update.birth_date = user_data.birth_date
        user_to_update.is_federated = user_data.is_federated
        user_to_update.weight_in_kg = user_data.weight_in_kg
        user_to_update.height_in_cm = user_data.height_in_cm
        user_to_update.is_admin=user_data.is_admin
        user_to_update.interests=user_data.interests
        self.users.append(user_to_update)

    def find_by_device_token(self, device_token: str) -> Optional[User]:
        """Get a user by device token"""
        for token in self.device_tokens:
            if token.device_token == device_token:
                return self.find_non_admin_by_username(token.username)

    def update_device_token(self, username: str, device_token: str):
        """Update a user's device token"""
        new_token = UserDeviceToken
        new_token.device_token = device_token
        new_token.username = username

        for token in self.device_tokens:
            if token.username == username:
                self.device_tokens.remove(token)
                break
        self.device_tokens.append(new_token)

    def remove_user_device_token(self, device_token: str):
        """Remove a user's device token"""
        for token in self.device_tokens:
            if token.device_token == device_token:
                self.device_tokens.remove(token)
                break

    def get_device_token(self, username: str) -> str:
        """Get a user's device token"""
        filtered = list(filter(lambda entry: entry.username == username, self.device_tokens))
        return filtered[0] if len(filtered) > 0 else None

    def increment_password_changes(self, username: str):
        """Increment password changes"""
        for user in self.users:
            if user.username == username:
                self.users.remove(user)
                user.password_changes += 1
                self.users.append(user)
                break

    def update_coordinates(self, username: str, coordinates: Coordinates):
        """Update a user's coordinates"""
        for user in self.users:
            if user.username == username:
                self.users.remove(user)
                user.latitude = coordinates.latitude
                user.longitude = coordinates.longitude
                self.users.append(user)
                break

    def update_user_last_login(self, username: str):
        """Update a user's last login"""
        for user in self.users:
            if user.username == username:
                self.users.remove(user)
                user.last_login = datetime.datetime.now()
                self.users.append(user)
                break
