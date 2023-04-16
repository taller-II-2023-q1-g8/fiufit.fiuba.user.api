"""User Domain Entity"""


class User():
    """User Domain Entity Definition"""
    def __init__(
        self,
        username: str,
        firstname: str,
    ):
        self.username: str = username
        self.firstname: str = firstname

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, User):
            return self.username == obj.username

        return False

    def name(self):
        """Returns the name of the user"""
        return self.firstname
