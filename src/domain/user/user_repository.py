from abc import ABC, abstractmethod
from typing import Optional
from src.domain.user.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def all_usernames(self) -> list:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, username: str):
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User):
        raise NotImplementedError