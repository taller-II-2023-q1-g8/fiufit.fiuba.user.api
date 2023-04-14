#Entity
class User():
    def __init__(
        self,
        username: str,
        firstname: str,
    ):
        self.username: str = username
        self.firstname: str = firstname

    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.username == o.username

        return False
