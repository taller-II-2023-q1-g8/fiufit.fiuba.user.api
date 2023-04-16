from src.usecase.user import UserService 
from src.infrastructure.models import user_dto

class FakeUserRepoAlwaysOk():
    def create(self, user_data):
        a = 1
       
    def find_by_email(self, email):
        return None
    
    def find_by_username(self, username):
        return None
    
    def delete(self, username):
        a = 1
     
    def update(self, user_data):
        a = 1
    
    def all_usernames(self):
        return []

class UserRepoAlwaysUsernameUnavailable(FakeUserRepoAlwaysOk): 
    def create(self, user_data):
        raise Exception("User already exists")
    
    def find_by_username(self, username):
        return 1

class UserRepoAlwaysEmailUnavailable(FakeUserRepoAlwaysOk):
    def find_by_email(self, username):
        return 1

class FakeAuthServiceAlwaysOk():
    def sign_up(self, email, password):
        a = 1

class FakeAuthServiceAlwaysError():
    def sign_up(self, email, password):
        raise Exception("Firebase Error")

user_data = user_dto.UserSignUpDTO(
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
    user_service = UserService(UserRepoAlwaysEmailUnavailable(), FakeAuthServiceAlwaysOk())
  
    try:
        user_service.wants_to_create_user(user_data)
    except Exception as e:
        assert e.status_code == 409
        assert e.detail == "Email already exists"

def used_username_raises_exception():
    user_service = UserService(UserRepoAlwaysUsernameUnavailable(), FakeAuthServiceAlwaysOk())
    try:
        user_service.wants_to_create_user(user_data)
    except Exception as e:
        assert e.status_code == 409
        assert e.detail == "Username already exists"

def auth_service_error_raises_exception():
    user_service = UserService(FakeUserRepoAlwaysOk(), FakeAuthServiceAlwaysError())
    try:
        user_service.wants_to_create_user(user_data)
    except Exception as e:
        assert e.status_code == 500
        assert e.detail == "Firebase Error"
