import datetime
import logging

import models
import repository


class WasteService:
    def __init__(self,
                 users: repository.UserRepository,
                 wastes: repository.WasteRepository,
                 logger: logging.Logger):
        self._users = users
        self._wastes = wastes
        self._logger = logger
        pass

    def _create_user(self, user: models.User):
        if not self._users.user_exists(user.id):
            self._users.create_user(user)
            self._logger.info("new user created: %d %s", user.id, user.user_name)

    def start(self, message: models.Message):
        try:
            self._create_user(message.from_user)
        except Exception as e:
            self._logger.error("error on start command", exc_info=e)

    def add_waste(self, message: models.Message) -> bool:
        try:
            self._create_user(message.from_user)
            text = message.text.split()
            if len(text) != 4:
                return False
            waste = models.Waste(text[1], int(float(text[2]) * 100), text[3], datetime.datetime.now())
            self._wastes.add_waste(message.from_user.id, waste)
            return True
        except Exception as e:
            self._logger.error("error on add command", exc_info=e)

    def get_history(self, message: models.Message) -> list[models.Waste]:
        try:
            self._create_user(message.from_user)
            return self._wastes.get_history(message.from_user.id)
        except Exception as e:
            self._logger.error("error on history command", exc_info=e)
            return []

    def get_report(self, message: models.Message) -> list[models.Report]:
        try:
            self._create_user(message.from_user)
            return self._wastes.get_report(message.from_user.id)
        except Exception as e:
            self._logger.error("error on report command", exc_info=e)
            return []
