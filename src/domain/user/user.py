"""User Domain Entity"""
from datetime import date


class User():
    """User Domain Entity Definition"""
    def __init__(
        self,
        username: str,
        firstname: str,
        lastname: str,
        phone_number: str,
        gender: str,
        birthdate: date,
        weight_in_kg: float,
        height_in_cm: float
    ):
        self.username: str = username
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.phone_number: str = phone_number
        self.gender: str = gender
        self.birthdate: date = birthdate
        self.weight_in_kg: float = weight_in_kg
        self.height_in_cm: float = height_in_cm

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, User):
            return self.username == obj.username

        return False

    def name(self):
        """Returns the name of the user"""
        return self.firstname
