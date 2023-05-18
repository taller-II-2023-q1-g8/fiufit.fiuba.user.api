""" Data Transfer Objects for User Model"""
import datetime
from pydantic import BaseModel


class UserDTO(BaseModel):
    """User Data Transfer Object"""
    username: str
    firstname: str
    lastname: str
    birth_date: datetime.date
    gender: str
    email: str
    phone_number: str
    weight_in_kg: float
    height_in_cm: float
    is_federated: bool
    is_admin: bool

class UserSignUpDTO(BaseModel):
    """User Data Transfer Object for Sign Up """
    username: str
    firstname: str
    lastname: str
    birth_date: datetime.date
    gender: str
    email: str
    phone_number: str
    password: str
    weight_in_kg: float
    height_in_cm: float
    is_federated: bool
    is_admin: bool
