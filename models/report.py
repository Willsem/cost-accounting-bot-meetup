class Report:
    category: str
    sum: int

    def __init__(self, category: str, sum: int):
        self.category = category
        self.sum = sum

    def __str__(self):
        return f'{self.category}: {self.sum / 100}'
