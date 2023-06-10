"""User API Router"""
from os import environ
from typing import Union
from fastapi import APIRouter, HTTPException
from src.infrastructure.auth_service_mock import MockAuthService
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO
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


@user_routes.post("/", status_code=204, response_description="Update an user")
async def wants_to_update_user(user_data: UserDTO):
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
async def wants_to_follow_user(follower_username: str, followed_username: str):
    """User wants to follow a user"""
    return user_service.wants_to_unfollow_user(follower_username, followed_username)


@user_routes.get(
    "/followed/{username}", status_code=200, response_description="Get followed users"
)
async def requests_followed_users(username: str):
    """User requests followed users"""
    return user_service.requests_followed_users(username)
