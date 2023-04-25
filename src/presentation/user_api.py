"""User API Router"""
from os import environ
from typing import Union
from fastapi import APIRouter, HTTPException
from src.infrastructure.auth_service_mock import MockAuthService
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO
from src.infrastructure.user_repository_postgresql import UserTable
from src.usecase.user import UserService
from src.infrastructure.firebase import FirebaseAuthService

auth_service = FirebaseAuthService() if environ.get("RENDER") is not None \
    else MockAuthService()

user_routes = APIRouter(prefix="/user")
user_repository = UserTable()
user_service = UserService(user_repository, auth_service) # Application Service

# Transaction Model
@user_routes.get("/usernames", status_code=200, response_description="Get usernames list")
async def requests_all_usernames(prefix: Union[str, None] = None):
    """User requests all usernames"""
    if prefix is not None:
        return user_service.requests_usernames_starting_with(prefix)
    else:
        return user_service.requests_all_usernames()

@user_routes.get("/", status_code=200,
                 response_description="Get users matching conditions")
async def requests_user_matching(
    username: Union[str, None] = None,
    email: Union[str, None] = None):
    
    """Queries users"""
    if username is not None:
        return user_service.requests_user_with_username(username)
    if email is not None:
        return user_service.requests_user_with_email(email)
    else:
        raise HTTPException(status_code=400, detail="No query parameters provided")

@user_routes.get("/", status_code=200, response_description="Get user by username")
async def requests_user_with_username(username: str):
    """User requests user with username"""
    return user_service.requests_user_with_username(username)

@user_routes.get("/with_email/{email}", status_code=200, response_description="Get user by email")
async def requests_user_with_email(email: str):
    """User requests user with email"""
    return user_service.requests_user_with_email(email)


@user_routes.put("/", status_code=201, response_description="Create a new user")
async def wants_to_create_user(user_data: UserSignUpDTO):
    """User wants to create a new user"""
    return user_service.wants_to_create_user(user_data)


@user_routes.delete("/{username}", status_code=204, response_description="Delete user by username")
async def wants_to_delete_user(username: str):
    """User wants to delete a user"""
    return user_service.wants_to_delete_user(username)


@user_routes.post("/", status_code=204, response_description="Update an user")
async def wants_to_update_user(user_data: UserDTO):
    """User wants to update an user"""
    return user_service.wants_to_update_user(user_data)
