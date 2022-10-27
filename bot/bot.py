from telebot import TeleBot
from telebot.types import Message
import logging

import cache
import models
import services


class WasteBot:
    def __init__(
            self, token: str, waste_service: services.WasteService, cache: cache.CacheService, logger: logging.Logger):
        self._logger = logger
        self._waste_service = waste_service
        self._cache = cache
        self._bot = TeleBot(token)
        self._create_handlers()

    def _create_handlers(self):
        @self._bot.message_handler(commands=['start'])
        def start(message: Message):
            self._logger.info("[%s, %d]: %s", message.from_user.username, message.from_user.id, message.text)
            self._waste_service.start(self._convert_message(message))
            self._bot.send_message(message.chat.id, 'Добро пожаловать, это бот учета трат\n'
                                                    '\n'
                                                    '/add <Название> <Сумма> <Категория> - добавление траты\n'
                                                    '/history - история всех трат\n'
                                                    '/report - отчет по категориям')

        @self._bot.message_handler(commands=['add'])
        def add(message: Message):
            self._logger.info("[%s, %d]: %s", message.from_user.username, message.from_user.id, message.text)
            self._cache.clear_key(message.from_user.id, "history")
            self._cache.clear_key(message.from_user.id, "report")
            was_added = self._waste_service.add_waste(self._convert_message(message))
            if was_added:
                self._bot.send_message(message.chat.id, 'Трата успешно добавлена')
            else:
                self._bot.send_message(message.chat.id, 'Ошибка при добавлении траты')

        @self._bot.message_handler(commands=['history'])
        def history(message: Message):
            self._logger.info("[%s, %d]: %s", message.from_user.username, message.from_user.id, message.text)
            msg = self._cache.get(message.from_user.id, "history")
            if msg is not None:
                self._bot.send_message(message.chat.id, msg)
                return
            self._logger.info("history didn't find in cache, send to service")
            wastes = self._waste_service.get_history(self._convert_message(message))
            if len(wastes) == 0:
                self._bot.send_message(message.chat.id, 'Не найдено трат')
            else:
                msg = ''
                for waste in wastes:
                    msg += str(waste) + '\n'
                self._cache.set(message.from_user.id, "history", msg)
                self._bot.send_message(message.chat.id, msg)

        @self._bot.message_handler(commands=['report'])
        def report(message: Message):
            self._logger.info("[%s, %d]: %s", message.from_user.username, message.from_user.id, message.text)
            msg = self._cache.get(message.from_user.id, "report")
            if msg is not None:
                self._bot.send_message(message.chat.id, msg)
                return
            self._logger.info("report didn't find in cache, send to service")
            reports = self._waste_service.get_report(self._convert_message(message))
            if len(reports) == 0:
                self._bot.send_message(message.chat.id, 'Не найдено трат')
            else:
                msg = ''
                for report in reports:
                    msg += str(report) + '\n'
                self._cache.set(message.from_user.id, "report", msg)
                self._bot.send_message(message.chat.id, msg)

        @self._bot.message_handler()
        def default(message: Message):
            self._logger.info("[%s, %d]: %s", message.from_user.username, message.from_user.id, message.text)
            self._bot.send_message(message.chat.id, 'Неизвестная команда')

    @staticmethod
    def _convert_message(message: Message) -> models.Message:
        return models.Message(
            models.User(
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username,
            ),
            message.text
        )

    def run(self):
        self._bot.polling(none_stop=True)
