import datetime
import pytest
from src.infrastructure.models.coordinates import Coordinates
from src.infrastructure.models.user_device import UserDeviceToken
from src.infrastructure.models.user_dto import UpdateUserDTO, UserSignUpDTO
from src.tests.mock_user_repository import MockUserRepository
from src.infrastructure.auth_service_mock import MockAuthService

from src.usecase.user import UserService

users_dicts = [
    {
        "username": "jankos",
        "firstname": "jankos",
        "lastname": "jankos",
        "birth_date": "2001-06-15",
        "gender": "male",
        "email": "jankos@p33.com",
        "phone_number": "12346643",
        "password": "lasdas332",
        "weight_in_kg": 80,
        "height_in_cm": 184,
        "is_federated": False,
        "is_admin": False,
        "interests": ["Pecho", "Correr"],
    },
    {
        "username": "freddy",
        "firstname": "freddy",
        "lastname": "mercury",
        "birth_date": "2001-06-15",
        "gender": "male",
        "email": "fred@p33.com",
        "phone_number": "12346643",
        "password": "lasdas332",
        "weight_in_kg": 80,
        "height_in_cm": 184,
        "is_federated": False,
        "is_admin": False,
        "interests": ["Natación", "Correr"],
    },
    {
        "username": "JohnT",
        "firstname": "John",
        "lastname": "Travolta",
        "birth_date": "2001-06-15",
        "gender": "male",
        "email": "johnny@p33.com",
        "phone_number": "12346643",
        "password": "lasdas332",
        "weight_in_kg": 80,
        "height_in_cm": 184,
        "is_federated": False,
        "is_admin": False,
        "interests": ["Correr"],
    },
    {
        "username": "admin",
        "firstname": "juan",
        "lastname": "perez",
        "birth_date": "2001-06-15",
        "gender": "male",
        "email": "admin@p33.com",
        "phone_number": "12346643",
        "password": "lasdas332",
        "weight_in_kg": 80,
        "height_in_cm": 184,
        "is_federated": False,
        "is_admin": True,
        "interests": [],
    },
]

users = []

for user_dict in users_dicts:
    user = UserSignUpDTO(
        created_at=datetime.datetime.now(),
        password_changes=0,
        last_login=None,
        password="lasdas332",
        username=user_dict["username"],
        firstname=user_dict["firstname"],
        lastname=user_dict["lastname"],
        email=user_dict["email"],
        phone_number=user_dict["phone_number"],
        gender=user_dict["gender"],
        birth_date=user_dict["birth_date"],
        is_federated=user_dict["is_federated"],
        weight_in_kg=user_dict["weight_in_kg"],
        height_in_cm=user_dict["height_in_cm"],
        is_admin=user_dict["is_admin"],
        interests=user_dict["interests"],
    )
    users.append(user)

tokens_dicts = [
    {"username": "jankos", "device_token": "dfkbnsdkhg"},
    {"username": "freddy", "device_token": "56yhfnsdkhg"},
]

tokens = []

for token_dict in tokens_dicts:
    token = UserDeviceToken(
        username=token_dict["username"], device_token=token_dict["device_token"]
    )
    tokens.append(token)


def test_requests_all_admins():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    assert user_service.requests_all_admin_users() == [users[3]]


def test_requests_all_admins_usernames():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    assert user_service.requests_all_admin_usernames() == ["admin"]


def test_requests_all_non_admins():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    assert user_service.requests_all_non_admin_users() == [users[0], users[1], users[2]]


def test_requests_all_non_admins_usernames():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    assert user_service.requests_all_non_admin_usernames() == [
        "jankos",
        "freddy",
        "JohnT",
    ]


def test_requests_non_admin_usernames_starting_with():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    assert user_service.requests_non_admin_usernames_starting_with("j") == ["jankos"]


def test_requests_admin_usernames_starting_with():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    assert user_service.requests_admin_usernames_starting_with("a") == ["admin"]


def test_requests_non_admin_user_with_username():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )
    assert user_service.requests_non_admin_user_with_username("jankos") == users[0]


def test_requests_non_admin_user_with_email():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    assert user_service.requests_non_admin_user_with_email("johnny@p33.com") == users[2]


def test_requests_admin_user_with_username():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    assert user_service.requests_admin_user_with_username("admin") == users[3]


def test_requests_admin_user_with_email():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    assert user_service.requests_admin_user_with_email("admin@p33.com") == users[3]


def test_wants_to_create_user():
    user_service = UserService(
        MockUserRepository([], []),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    user_service.wants_to_create_user(users[0])
    assert len(user_service.requests_all_non_admin_users()) == 1


def test_wants_to_delete_user():
    user_backup = users[0]

    user_service = UserService(
        MockUserRepository(users, []),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    user_service.wants_to_delete_user(users[0].username)
    assert len(user_service.requests_all_non_admin_users()) == 2
    user_service.wants_to_create_user(user_backup)


def test_wants_to_update_user():
    user_service = UserService(
        MockUserRepository(users, []),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    update_data = UpdateUserDTO(
        username="jankos",
        email="qdwqjqjf@gmasda.com",
        birth_date=datetime.datetime(1999, 1, 1),
        weight_in_kg=100,
        height_in_cm=200,
        interests=[],
        firstname="Jan",
        lastname="Kowalski",
        gender="male",
        is_admin=False,
        is_federated=False,
        phone_number="123456789",
    )

    user_service.wants_to_update_user(update_data)
    assert (
        user_service.requests_non_admin_user_with_email("qdwqjqjf@gmasda.com")
        is not None
    )


def test_wants_to_update_device_token():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    user_service.wants_to_update_device_token("jankos", "new_token")
    assert user_service.requests_device_token_for_user("jankos") == "new_token"


def test_wants_to_update_last_login():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    user_service.wants_to_update_last_login("jankos")
    previous_login = user_service.requests_non_admin_user_with_username(
        "jankos"
    ).last_login

    user_service.wants_to_update_last_login("jankos")
    assert (
        user_service.requests_non_admin_user_with_username("jankos").last_login
        > previous_login
    )


def test_wants_to_increment_password_changes():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    user_service.wants_to_increment_password_changes("jankos")
    assert (
        user_service.requests_non_admin_user_with_username("jankos").password_changes
        == 1
    )


def test_wants_to_update_coordinates():
    user_service = UserService(
        MockUserRepository(users, tokens),
        auth_service=MockAuthService(),
        notification_service=None,
        follow_repository=None,
        block_repository=None,
    )

    new_coords = Coordinates(latitude=1.0, longitude=1.0)

    user_service.wants_to_update_coordinates("jankos", new_coords)
    assert user_service.requests_non_admin_user_with_username("jankos").latitude == 1.0
    assert user_service.requests_non_admin_user_with_username("jankos").longitude == 1.0
