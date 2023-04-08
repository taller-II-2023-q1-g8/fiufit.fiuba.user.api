from pydantic import BaseModel
import datetime

class UserDTO(BaseModel):
    id: str
    firstname: str
    birth_date: datetime.date
    gender: str
    email: str
    phone_number: str

class UserSignUpDTO(BaseModel):
    id: str
    firstname: str
    birth_date: datetime.date
    gender: str
    email: str
    phone_number: str
    password: str


