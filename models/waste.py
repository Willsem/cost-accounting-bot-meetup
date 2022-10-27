import datetime
import uuid


class Waste:
    id: uuid.UUID
    name: str
    cost: int
    category: str
    date: datetime.datetime
    user_wastes: int

    def __init__(self, name: str, cost: int, category: str, date: datetime.datetime):
        self.name = name
        self.cost = cost
        self.category = category
        self.date = date

    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y %H:%M:%S")} {self.name} ({self.category}): {self.cost / 100} Руб.'
