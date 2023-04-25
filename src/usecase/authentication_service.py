from abc import abstractmethod


class IAuthenticationService:
    @abstractmethod
    def signup(self, email: str, password: str):
        """Sign up a new user"""
        raise NotImplementedError
