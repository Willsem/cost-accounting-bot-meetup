import uuid

import psycopg2

import models


class WasteRepository:
    def __init__(self, connect):
        self.client: psycopg2.connect = connect

    def add_waste(self, user_id: int, waste: models.Waste):
        waste.id = uuid.uuid4()
        with self.client.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "wastes" '
                '("id", "name", "cost", "category", "date", "user_wastes") '
                'VALUES (%(id)s, %(name)s, %(cost)s, %(category)s, %(date)s, %(user_wastes)s)',
                {
                    'id': str(waste.id),
                    'name': waste.name,
                    'cost': waste.cost,
                    'category': waste.category,
                    'date': waste.date,
                    'user_wastes': user_id,
                }
            )
        self.client.commit()

    def get_history(self, user_id: int) -> list[models.Waste]:
        with self.client.cursor() as cursor:
            cursor.execute(
                'SELECT "id", "name", "cost", "category", "date" FROM "wastes" '
                'WHERE "user_wastes"=%(user_id)s',
                {
                    'user_id': user_id,
                }
            )
            wastes = list()
            for row in cursor:
                wastes.append(
                    models.Waste(row[1], row[2], row[3], row[4])
                )
            return wastes

    def get_report(self, user_id: int) -> list[models.Report]:
        with self.client.cursor() as cursor:
            cursor.execute(
                'SELECT "category", SUM("cost") FROM "wastes" '
                'WHERE "user_wastes"=%(user_id)s '
                'GROUP BY "category" '
                'ORDER BY SUM("cost") DESC',
                {
                    'user_id': user_id,
                }
            )
            reports = list()
            for report in cursor:
                reports.append(models.Report(report[0], report[1]))
            return reports
