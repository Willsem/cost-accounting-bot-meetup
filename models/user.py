class User:
    id: int
    first_name: str
    last_name: str
    user_name: str

    def __init__(self, id: int, first_name: str, last_name: str, user_name: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
