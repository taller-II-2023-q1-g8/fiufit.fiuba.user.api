from fastapi import APIRouter
from src.infrastructure.models.user_dto import UserDTO, UserSignUpDTO
from src.infrastructure.user_repository_postgresql import UserTable
from src.usecase.user import UserService


user_routes = APIRouter(prefix="/user")
user_repository = UserTable()
user_service = UserService(UserTable)

#Transaction Model
@user_routes.get("/{id}")
async def requests_user_with_id(id: str):
    return user_service.requests_user_with_id(id)

@user_routes.put("/", status_code=201)   
async def wants_to_create_user(user_data: UserSignUpDTO):
    return user_service.wants_to_create_user(user_data)