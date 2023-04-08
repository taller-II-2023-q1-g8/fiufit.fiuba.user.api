from typing import Optional
from src.domain.user.user_repository import UserRepository
from src.infrastructure.database import SessionLocal
from src.infrastructure.models.user import UserModel
from src.infrastructure.models.user_dto import UserSignUpDTO
from src.domain.user.user import User

class UserTable(UserRepository):
    def find_by_id(self, id: str) -> Optional[User]:
        session = SessionLocal()
        return session.query(UserModel).filter(UserModel.id == id).first()

    def create(self, user_data: UserSignUpDTO) -> Optional[User]:
        session = SessionLocal()
        session.add(UserModel(
            id=user_data.id, 
            firstname=user_data.firstname,
            email=user_data.email,
            phone_number=user_data.phone_number,
            gender=user_data.gender,
            birth_date=user_data.birth_date))
        session.commit()
