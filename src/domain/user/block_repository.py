"""Block Repository Interface"""
from abc import ABC, abstractmethod
from typing import Optional
from src.infrastructure.models.blocked_user import BlockedUserModel

class IBlockRepository(ABC):
    @abstractmethod
    def create(self, blocked_username, admin_username) -> None:
        """Block a user"""
        raise NotImplementedError

    @abstractmethod
    def remove(self, username: str) -> None:
        """Remove a block"""
        raise NotImplementedError

    @abstractmethod
    def find_by_blocked_username(self, username: str) -> BlockedUserModel | None:
        """Find a user's followers"""
        raise NotImplementedError