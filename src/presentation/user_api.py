"""User API Router"""
from os import environ
from typing import Union
from fastapi import APIRouter, HTTPException
from src.infrastructure.auth_service_mock import MockAuthService
from src.infrastructure.models.coordinates import Coordinates
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO, UpdateUserDTO
from src.infrastructure.models.user_device_token_dto import UserDeviceTokenDTO
from src.infrastructure.user_repository_postgresql import UserTable
from src.usecase.user import UserService
from src.infrastructure.firebase import FirebaseAuthService

auth_service = (
    FirebaseAuthService() if environ.get("RENDER") is not None else MockAuthService()
)

user_routes = APIRouter(prefix="/user")
user_repository = UserTable()
user_service: UserService = UserService(
    user_repository, auth_service
)  # Application Service


# Transaction Model
@user_routes.get(
    "/usernames", status_code=200, response_description="Get non-admin usernames list"
)
async def requests_all_non_admin_usernames(prefix: Union[str, None] = None):
    """User requests all usernames"""
    if prefix is not None:
        return user_service.requests_non_admin_usernames_starting_with(prefix)
    else:
        return user_service.requests_all_non_admin_usernames()


@user_routes.get(
    "/admin/usernames",
    status_code=200,
    response_description="Get admins usernames list",
)
async def requests_all_admin_usernames(prefix: Union[str, None] = None):
    """User requests all usernames"""
    if prefix is not None:
        return user_service.requests_admin_usernames_starting_with(prefix)
    else:
        return user_service.requests_all_admin_usernames()


@user_routes.get(
    "/", status_code=200, response_description="Get non-admin users matching conditions"
)
async def requests_user_matching(
    username: Union[str, None] = None, email: Union[str, None] = None
):
    """Queries users"""
    if username is not None:
        return user_service.requests_non_admin_user_with_username(username)
    if email is not None:
        return user_service.requests_non_admin_user_with_email(email)
    else:
        return user_service.requests_all_non_admin_users()


@user_routes.get(
    "/admin",
    status_code=200,
    response_description="Get admin users matching conditions",
)
async def requests_user_matching(
    username: Union[str, None] = None, email: Union[str, None] = None
):
    """Queries users"""
    if username is not None:
        return user_service.requests_admin_user_with_username(username)
    if email is not None:
        return user_service.requests_admin_user_with_email(email)
    else:
        return user_service.requests_all_admin_users()


@user_routes.put(
    "/login/{username}", status_code=200, response_description="Update last login"
)
async def wants_to_update_last_login(username: str):
    """User wants to update last login time"""
    return user_service.wants_to_update_last_login(username)


@user_routes.put(
    "/device/{username}", status_code=200, response_description="Update device token"
)
async def wants_to_update_device_token(username: str, body: UserDeviceTokenDTO):
    """User wants to update device token"""
    return user_service.wants_to_update_device_token(username, body.device_token)


@user_routes.get(
    "/device/{username}",
    status_code=200,
    response_description="Get device token for user",
)
async def requests_user_device_token(username: str):
    """User wants to update device token"""
    return user_service.requests_device_token_for_user(username)


@user_routes.put("/", status_code=201, response_description="Create a new user")
async def wants_to_create_user(user_data: UserSignUpDTO):
    """User wants to create a new user"""
    return user_service.wants_to_create_user(user_data)


@user_routes.put("/admin", status_code=201, response_description="Create a new admin")
async def wants_to_create_admin(user_data: UserSignUpDTO):
    """User wants to create a new user"""
    return user_service.wants_to_create_admin(user_data)


@user_routes.delete(
    "/{username}", status_code=204, response_description="Delete user by username"
)
async def wants_to_delete_user(username: str):
    """User wants to delete a user"""
    return user_service.wants_to_delete_user(username)


@user_routes.post("/", status_code=200, response_description="Update an user")
async def wants_to_update_user(user_data: UpdateUserDTO):
    """User wants to update an user"""
    return user_service.wants_to_update_user(user_data)


@user_routes.post(
    "/follow/{follower_username}/{followed_username}",
    status_code=200,
    response_description="Follow a user",
)
async def wants_to_follow_user(follower_username: str, followed_username: str):
    """User wants to follow a user"""
    return user_service.wants_to_follow_user(follower_username, followed_username)


@user_routes.delete(
    "/follow/{follower_username}/{followed_username}",
    status_code=200,
    response_description="Unfollow a user",
)
async def wants_to_unfollow_user(follower_username: str, followed_username: str):
    """User wants to follow a user"""
    return user_service.wants_to_unfollow_user(follower_username, followed_username)


@user_routes.get(
    "/followed/{username}", status_code=200, response_description="Get followed users"
)
async def requests_followed_users(username: str):
    """User requests followed users"""
    return user_service.requests_followed_users(username)


@user_routes.get(
    "/follower/{username}", status_code=200, response_description="Get follower users"
)
async def requests_follower_users(username: str):
    """User requests follower users"""
    return user_service.requests_follower_users(username)


@user_routes.get(
    "/blocked/{username}", status_code=200, response_description="Get follower users"
)
async def asks_if_user_is_blocked(username: str):
    """User asks if user is blocked"""
    return user_service.asks_if_user_is_blocked(username)


@user_routes.post(
    "/block/{username}/{admin_username}",
    status_code=200,
    response_description="Block user",
)
async def wants_to_block_user(username: str, admin_username: str):
    """User wants to block user"""
    return user_service.wants_to_block_user(username, admin_username)


@user_routes.post(
    "/unblock/{username}", status_code=200, response_description="Unblock user"
)
async def wants_to_unblock_user(username: str):
    """User wants to unblock user"""
    return user_service.wants_to_unblock_user(username)

@user_routes.post(
    "/changed-password/{username}", status_code=200, response_description="Password changes incremented"
)
async def wants_to_increment_password_changes(username: str):
    """User wants to increment password changes"""
    return user_service.wants_to_increment_password_changes(username)

@user_routes.put(
    "/coordinates/{username}", status_code=200, response_description="Update user coordinates"
)
async def wants_to_update_user_coordinates(username: str, coordinates: Coordinates):
    """User wants to update his coordinates"""
    return user_service.wants_to_update_coordinates(username, coordinates)