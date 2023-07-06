from os import environ
from src.infrastructure.block_repository_postgresql import BlockRepositoryPostreSQL
from src.infrastructure.firebase import FirebaseAuthService
from src.infrastructure.auth_service_mock import MockAuthService
from src.infrastructure.follow_repository_postgresql import FollowRepositoryPostgreSQL
from src.infrastructure.notification_service import NotificationService
from src.infrastructure.user_repository_postgresql import UserTable
from src.usecase.user import UserService
from src.infrastructure.database import SessionLocal

auth_service = (
    FirebaseAuthService() if environ.get("RENDER") is not None else MockAuthService()
)

user_repository = UserTable(SessionLocal)
notification_service = NotificationService()
follow_repository = FollowRepositoryPostgreSQL(SessionLocal)
block_repository = BlockRepositoryPostreSQL(SessionLocal)

user_service: UserService = UserService(
    user_repository,
    auth_service,
    notification_service,
    follow_repository,
    block_repository,
) 
