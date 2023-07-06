"""User Repository Implementation for PostgreSQL"""
import datetime
from typing import Optional
from src.domain.user.follow_repository import IFollowRepository
from src.infrastructure.database import SessionLocal
from src.infrastructure.models.follow import FollowModel

class FollowRepositoryPostgreSQL(IFollowRepository):
    """Repository Definition"""

    def __init__(self, session):
        self.session = session

    def create(self, follower_username, followed_username) -> None:
        """Create a new user"""

        if self.find_by_pair(follower_username, followed_username):
            return None

        session = self.session()
        session.add(FollowModel(
            follower_username=follower_username,
            followed_username=followed_username,
        ))
        session.commit()

    def remove(self, follow: FollowModel) -> None:
        """Remove a user"""
        session = self.session()
        session.delete(follow)
        session.commit()

    def find_by_follower_username(self, username: str) -> list[FollowModel]:
        """Find a user's followers"""
        session = self.session()
        results = session.query(FollowModel).filter(FollowModel.follower_username == username).all()
        return list(results) if results else []

    def find_by_following_username(self, username: str) -> list[FollowModel]:
        """Find a users who follow a specific user"""
        session = self.session()
        results = session.query(FollowModel).filter(FollowModel.followed_username == username).all()
        return list(results) if results else []
    
    def find_by_pair(self, follower_username: str, following_username: str) -> FollowModel | None:
        """Find a specific follow"""
        session = self.session()
        return session.query(FollowModel).filter(
            FollowModel.follower_username == follower_username,
            FollowModel.followed_username == following_username
        ).first()