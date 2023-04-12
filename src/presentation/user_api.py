from fastapi import APIRouter, exceptions
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO
from src.infrastructure.user_repository_postgresql import UserTable
from src.infrastructure.firebase import sign_up as firebase_sign_up
from src.usecase.user import UserService


user_routes = APIRouter(prefix="/user")
user_repository = UserTable()
user_service = UserService(user_repository)

# Transaction Model
@user_routes.get("/", status_code=200, response_description="Get user id list")
async def requests_user_list():
    return user_service.requests_all_user_ids()

@user_routes.get("/{id}", status_code=200, response_description="Get user by id")
async def requests_user_with_id(id: str):
    return user_service.requests_user_with_id(id)


@user_routes.put("/", status_code=201, response_description="Create a new user")
async def wants_to_create_user(user_data: UserSignUpDTO):
    try:
        firebase_sign_up(user_data.email, user_data.password)
    except:
        raise exceptions.HTTPException(status_code=406, detail="[FIREBASE] email already exists")
    
    return user_service.wants_to_create_user(user_data)


@user_routes.delete("/{id}", status_code=204, response_description="Delete user by id")
async def wants_to_delete_user(id: str):
    return user_service.wants_to_delete_user(id)


@user_routes.post("/", status_code=204, response_description="Update an user")
async def wants_to_update_user(user_data: UserDTO):
    return user_service.wants_to_update_user(user_data)
