#Entity
class User():
    def __init__(
        self,
        id: str,
        firstname: str,
    ):
        self.id: str = id
        self.firstname: str = firstname

    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.id == o.id

        return False
