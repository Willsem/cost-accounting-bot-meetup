import redis


class CacheService:
    def __init__(self, client: redis.Redis):
        self.client = client

    def get(self, user_id: int, message: str) -> str | None:
        try:
            return self.client.get(self.generate_key(user_id, message))
        except:
            return None

    def set(self, user_id: int, message: str, content: str):
        try:
            self.client.set(self.generate_key(user_id, message), content)
        except:
            pass

    def clear_key(self, user_id: int, message: str):
        try:
            self.client.delete(self.generate_key(user_id, message))
        except:
            pass

    @staticmethod
    def generate_key(user_id: int, message: str) -> str:
        return f'{user_id}:{message}'
