from typing import Optional
from ddd.domain.user.user_repository import UserRepository
from ddd.infrastructure.database import SessionLocal
from ddd.infrastructure.models import UserModel
from ddd.infrastructure.user_dto import UserDTO
from ddd.domain.user.user import User

class UserTable(UserRepository):
    def find_by_id(self, id: str) -> Optional[User]:
        session = SessionLocal()
        return session.query(UserModel).filter(UserModel.id == id).first()

    def create(self, user_data: UserDTO) -> Optional[User]:
        session = SessionLocal()
        session.add(UserModel(
            id=user_data.id, 
            firstname=user_data.firstname))
        session.commit()
