"""Follow Repository Interface"""
from abc import ABC, abstractmethod
from typing import Optional
from src.infrastructure.models.follow import FollowModel


class IFollowRepository(ABC):
    @abstractmethod
    def create(self, follower_username, followed_username) -> None:
        """Create a new user"""
        raise NotImplementedError

    @abstractmethod
    def remove(self, follower: str, following: str) -> None:
        """Remove a user"""
        raise NotImplementedError

    @abstractmethod
    def find_by_follower_username(self, username: str) -> list[FollowModel]:
        """Find a user's followers"""
        raise NotImplementedError

    @abstractmethod
    def find_by_following_username(self, username: str) -> list[FollowModel]:
        """Find a users who follow a specific user"""
        raise NotImplementedError
    
    @abstractmethod
    def find_by_pair(self, follower_username: str, following_username: str) -> FollowModel | None:
        """Find a specific follow"""
        raise NotImplementedError