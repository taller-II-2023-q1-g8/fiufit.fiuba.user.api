import datetime
from src.domain.user.block_repository import IBlockRepository
from src.infrastructure.models.blocked_user import BlockedUserModel


class BlockRepositoryPostreSQL(IBlockRepository):
    def __init__(self, session):
        self.session = session

    def create(self, blocked_username, admin_username) -> None:
        """Block a user"""
        if self.find_by_blocked_username(blocked_username):
            return None

        session = self.session()
        session.add(
            BlockedUserModel(
                blocked_user=blocked_username,
                blocked_by=admin_username,
                created_at=datetime.datetime.now(),
            )
        )
        session.commit()

    def remove(self, block: BlockedUserModel) -> None:
        """Remove a block"""
        session = self.session()
        session.delete(block)
        session.commit()

    def find_by_blocked_username(self, username: str) -> BlockedUserModel | None:
        """Find a user's followers"""
        session = self.session()
        return (
            session.query(BlockedUserModel)
            .filter(BlockedUserModel.blocked_user == username)
            .first()
        )
