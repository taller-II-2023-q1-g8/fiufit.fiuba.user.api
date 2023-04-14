from fastapi import APIRouter, exceptions
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO
from src.infrastructure.user_repository_postgresql import UserTable
from src.infrastructure.firebase import sign_up as fb_sign_up
from src.usecase.user import UserService


user_routes = APIRouter(prefix="/user")
user_repository = UserTable()
user_service = UserService(user_repository)

# Transaction Model
@user_routes.get("/", status_code=200, response_description="Get usernames list")
async def requests_user_list():
    return user_service.requests_all_usernames()

@user_routes.get("/{username}", status_code=200, response_description="Get user by username")
async def requests_user_with_username(username: str):
    return user_service.requests_user_with_username(username)


@user_routes.put("/", status_code=201, response_description="Create a new user")
async def wants_to_create_user(user_data: UserSignUpDTO):
    if user_repository.find_by_email(user_data.email) is None:
        user_service.wants_to_create_user(user_data)
        try:
            fb_sign_up(user_data.email, user_data.password)
        except:
            user_repository.delete(user_data.username)
            raise exceptions.HTTPException(status_code=406, detail="[ERROR] email registered in firebase, but is not in application database")
    else:
        raise exceptions.HTTPException(status_code=406, detail="email in use")


@user_routes.delete("/{username}", status_code=204, response_description="Delete user by username")
async def wants_to_delete_user(username: str):
    return user_service.wants_to_delete_user(username)


@user_routes.post("/", status_code=204, response_description="Update an user")
async def wants_to_update_user(user_data: UserDTO):
    return user_service.wants_to_update_user(user_data)
