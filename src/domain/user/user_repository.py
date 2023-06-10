"""User Repository Interface"""
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.user.user import User
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO


class IUserRepository(ABC):
    """User Repository Interface Definition"""
    @abstractmethod
    def create(self, user_data: UserSignUpDTO) -> Optional[User]:
        """Create a new user"""
        raise NotImplementedError

    @abstractmethod
    def all_non_admin(self) -> list:
        """Get all non-admin users"""
        raise NotImplementedError

    @abstractmethod
    def all_admins(self) -> list:
        """Get all admin users"""
        raise NotImplementedError

    @abstractmethod
    def all_non_admin_usernames(self) -> list:
        """Get all non-admin usernames"""
        raise NotImplementedError

    @abstractmethod
    def all_admin_usernames(self) -> list:
        """Get all admin usernames"""
        raise NotImplementedError

    @abstractmethod
    def non_admin_usernames_starting_with(self, prefix: str) -> list:
        """Get non-admin usernames starting with"""
        raise NotImplementedError

    @abstractmethod
    def admin_usernames_starting_with(self, prefix: str) -> list:
        """Get admin usernames starting with"""
        raise NotImplementedError

    @abstractmethod
    def find_non_admin_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        raise NotImplementedError

    @abstractmethod
    def find_non_admin_by_username(self, username: str) -> Optional[User]:
        """Find a user by username"""
        raise NotImplementedError

    @abstractmethod
    def find_admin_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        raise NotImplementedError

    @abstractmethod
    def find_admin_by_username(self, username: str) -> Optional[User]:
        """Find a user by username"""
        raise NotImplementedError

    @abstractmethod
    def delete(self, username: str):
        """Delete a user by username"""
        raise NotImplementedError

    @abstractmethod
    def update(self, user_data: UserDTO):
        """Update a user"""
        raise NotImplementedError
