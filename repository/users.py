import psycopg2

import models


class UserRepository:
    def __init__(self, connect):
        self.client: psycopg2.connect = connect

    def user_exists(self, user_id: int) -> bool:
        with self.client.cursor() as cursor:
            cursor.execute(
                'SELECT count(*) FROM "users" WHERE "id"=%(user_id)s',
                {'user_id': user_id},
            )
            for row in cursor:
                return row[0] > 0

    def create_user(self, user: models.User):
        with self.client.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "users" '
                '("id", "first_name", "last_name", "user_name") '
                'VALUES (%(id)s, %(first_name)s, %(last_name)s, %(username)s)',
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.user_name,
                }
            )
        self.client.commit()
