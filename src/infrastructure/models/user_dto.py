""" Data Transfer Objects for User Model"""

import datetime
from pydantic import BaseModel


class UserDTO(BaseModel):
    """User Data Transfer Object"""
    username: str
    firstname: str
    birth_date: datetime.date
    gender: str
    email: str
    phone_number: str

class UserSignUpDTO(BaseModel):
    """User Data Transfer Object for Sign Up """
    username: str
    firstname: str
    birth_date: datetime.date
    gender: str
    email: str
    phone_number: str
    password: str
