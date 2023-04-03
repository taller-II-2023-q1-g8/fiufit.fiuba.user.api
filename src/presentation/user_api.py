from fastapi import APIRouter
from src.infrastructure.models.user_dto import UserDTO
from src.infrastructure.user_repository_postgresql import UserTable
import src.usecase.user as use_case

user_routes = APIRouter(prefix="/user")
user_repository = UserTable()

#Transaction Model
@user_routes.get("/{id}")
async def requests_user_with_id(id: str):
    return use_case.requests_user_with_id(id)

@user_routes.put("/")
async def wants_to_create_user(user_data: UserDTO):
    use_case.wants_to_create_user(user_data)