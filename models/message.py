import models


class Message:
    text: str
    from_user: models.User

    def __init__(self, from_user: models.User, text: str):
        self.from_user = from_user
        self.text = text
