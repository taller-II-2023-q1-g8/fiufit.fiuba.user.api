from abc import ABC, abstractmethod
from typing import Optional
from src.domain.user.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User):
        raise NotImplementedError