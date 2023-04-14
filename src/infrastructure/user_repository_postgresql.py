from typing import Optional
from src.domain.user.user_repository import UserRepository
from src.infrastructure.database import SessionLocal
from src.infrastructure.models.user import UserModel
from src.infrastructure.models.user_dto import UserSignUpDTO, UserDTO
from src.domain.user.user import User


class UserTable(UserRepository):
    def all_usernames(self):
        session = SessionLocal()
        return list(map(lambda user: user.username, session.query(UserModel).all()))

    def find_by_username(self, username: str) -> Optional[User]:
        session = SessionLocal()
        return session.query(UserModel).filter(UserModel.username == username).first()

    def find_by_email(self, email: str) -> Optional[User]:
        session = SessionLocal()
        return session.query(UserModel).filter(UserModel.email == email).first()

    def create(self, user_data: UserSignUpDTO) -> Optional[User]:
        session = SessionLocal()
        session.add(UserModel(
            username=user_data.username, 
            firstname=user_data.firstname,
            email=user_data.email,
            phone_number=user_data.phone_number,
            gender=user_data.gender,
            birth_date=user_data.birth_date))
        session.commit()

    def delete(self, username: str):
        session = SessionLocal()
        user_to_delete = session.query(UserModel).filter(UserModel.username == username).first()
        session.delete(user_to_delete)
        session.commit()

    def update(self, user_data: UserDTO):
        session = SessionLocal()
        user_to_update = session.query(UserModel).filter(UserModel.username == user_data.username).first()
        user_to_update.username = user_data.username
        user_to_update.firstname = user_data.firstname
        user_to_update.email = user_data.email
        user_to_update.phone_number = user_data.phone_number
        user_to_update.gender = user_data.gender
        user_to_update.birth_date = user_data.birth_date
        session.commit()
