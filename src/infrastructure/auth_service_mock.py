from src.usecase.authentication_service import IAuthenticationService


class MockAuthService(IAuthenticationService):

    def sign_up(self, email: str, password: str):
        pass
