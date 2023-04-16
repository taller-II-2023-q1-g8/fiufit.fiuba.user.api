"""Tests for the user module"""
from fastapi import HTTPException
from src.domain.user.user_repository import IUserRepository
from src.usecase.user import UserService
from src.infrastructure.models.user_dto import UserSignUpDTO


class FakeUserRepoAlwaysOk(IUserRepository):
    """Fake User Repository that does Nothing"""

    def create(self, user_data):
        """Returns None"""
        # pylint: disable=unused-argument
        return None

    def find_by_email(self, email):
        """Returns None"""
        # pylint: disable=unused-argument
        return None
    def find_by_username(self, username):
        """Returns None"""
        # pylint: disable=unused-argument
        return None

    def delete(self, username):
        """Returns  None"""
        # pylint: disable=unused-argument
        return None

    def update(self, user_data):
        """returns None"""
        # pylint: disable=unused-argument
        return None
    def all_usernames(self):
        """Returns an empty list"""
        # pylint: disable=unused-argument
        return []

class UserRepoAlwaysUsernameUnavailable(FakeUserRepoAlwaysOk):
    """User Repository that always raises an exception when trying\
        to create a user because of existing username"""
    def create(self, user_data):
        """Create a new user"""
        # pylint: disable=unused-argument
        raise Exception("User already exists")

    def find_by_username(self, username):
        """Always return something that isn't None"""
        return 1

class UserRepoAlwaysEmailUnavailable(FakeUserRepoAlwaysOk):
    """User Repository that always raises an exception when trying\
         to create a user because of existing email"""
    def find_by_email(self, email):
        """Always return something that isn't None"""
                # pylint: disable=unused-argument
        return 1

class FakeAuthServiceAlwaysOk():
    """Fake Auth Service that raises no Exceptions"""
    def sign_up(self, email, password):
        """Does nothing"""
        # pylint: disable=unused-argument
        return None
class FakeAuthServiceAlwaysError():
    """Fake Auth Service that always raises an exception"""
    def sign_up(self, email, password):
        """Raise an exception"""
        # pylint: disable=unused-argument
        raise Exception("Firebase Error")

test_user_data = UserSignUpDTO(
    username="matador",
    firstname="Juan",
    birth_date="1990-01-01",
    gender="male",
    email="cincuenta@gmail.com",
    phone_number="123456789",
    password="345tgi"
    )

#Tests
def used_email_raises_exception():
    """Tests that the user service raises an exception when\
          trying to create a user with an email that already exists"""
    user_service = UserService(UserRepoAlwaysEmailUnavailable(), FakeAuthServiceAlwaysOk())

    try:
        user_service.wants_to_create_user(test_user_data)
    except HTTPException as exc:
        assert exc.status_code == 409
        assert exc.detail == "Email already exists"

def used_username_raises_exception():
    """Tests that the user service raises an exception when trying \
        to create a user with an username that already exists"""
    user_service = UserService(UserRepoAlwaysUsernameUnavailable(), FakeAuthServiceAlwaysOk())
    try:
        user_service.wants_to_create_user(test_user_data)
    except HTTPException as exc:
        assert exc.status_code == 409
        assert exc.detail == "Username already exists"

def auth_service_error_raises_exception():
    """Tests that the user service raises an exception when trying \
        to create a user and the auth service raises an exception"""
    user_service = UserService(FakeUserRepoAlwaysOk(), FakeAuthServiceAlwaysError())
    try:
        user_service.wants_to_create_user(test_user_data)
    except HTTPException as exc:
        assert exc.status_code == 500
        assert exc.detail == "Firebase Error"
