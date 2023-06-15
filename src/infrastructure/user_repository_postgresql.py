"""User Repository Implementation for PostgreSQL"""
import datetime
from typing import Optional
from src.domain.user.user_repository import IUserRepository
from src.infrastructure.database import SessionLocal
from src.infrastructure.models.user import UserModel
from src.infrastructure.models.user_dto import UserSignUpDTO, UserDTO
from src.domain.user.user import User


class UserTable(IUserRepository):
    """Repository Definition"""

    def all_non_admin(self) -> list:
        """Get all non-admin users"""
        session = SessionLocal()
        return session.query(UserModel).filter(UserModel.is_admin == False).all()

    def all_admins(self) -> list:
        """Get all admin users"""
        session = SessionLocal()
        return session.query(UserModel).filter(UserModel.is_admin == True).all()

    def all_non_admin_usernames(self):
        """Get all non-admin usernames"""
        session = SessionLocal()
        admin = session.query(UserModel).filter(UserModel.is_admin == False).all()
        return list(map(lambda user: user.username, admin))

    def all_admin_usernames(self):
        """Get all admin usernames"""
        session = SessionLocal()
        admin = session.query(UserModel).filter(UserModel.is_admin == True).all()
        return list(map(lambda user: user.username, admin))

    def non_admin_usernames_starting_with(self, prefix: str) -> list:
        """Get non-admin usernames starting with"""
        all_usernames = self.all_non_admin_usernames()
        return list(filter(
            lambda username: username.startswith(prefix), all_usernames
            )
        )

    def admin_usernames_starting_with(self, prefix: str) -> list:
        """Get admin usernames starting with"""
        all_usernames = self.all_admin_usernames()
        return list(filter(
            lambda username: username.startswith(prefix), all_usernames
            )
        )

    def find_non_admin_by_username(self, username: str) -> Optional[User]:
        """Find a user by username"""
        session = SessionLocal()
        return session.query(UserModel)\
            .filter(UserModel.username == username)\
            .filter(UserModel.is_admin == False)\
            .first()

    def find_non_admin_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        session = SessionLocal()
        return session.query(UserModel)\
            .filter(UserModel.email == email)\
            .filter(UserModel.is_admin == False)\
            .first()

    
    def find_admin_by_username(self, username: str) -> Optional[User]:
        """Find a user by username"""
        session = SessionLocal()
        return session.query(UserModel)\
            .filter(UserModel.username == username)\
            .filter(UserModel.is_admin == True)\
            .first()

    def find_admin_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        session = SessionLocal()
        return session.query(UserModel)\
            .filter(UserModel.email == email)\
            .filter(UserModel.is_admin == True)\
            .first()

    def create(self, user_data: UserSignUpDTO) -> Optional[User]:
        """Create a new user"""
        session = SessionLocal()
        session.add(UserModel(
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
            is_admin=user_data.is_admin
            ))
        session.commit()

    def delete(self, username: str):
        """Delete a user by username"""
        session = SessionLocal()
        user_to_delete = session.query(UserModel).filter(UserModel.username == username).first()
        session.delete(user_to_delete)
        session.commit()

    def update(self, user_data: UserDTO):
        """Update a user"""
        session = SessionLocal()
        user_to_update = session.query(UserModel)\
            .filter(UserModel.username == user_data.username)\
            .first()
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
        session.commit()
