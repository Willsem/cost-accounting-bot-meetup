import logging
import json


class JsonFormatter(logging.Formatter):
    def __init__(self, fmt_dict: dict = None, time_format: str = "%Y-%m-%dT%H:%M:%S", msec_format: str = "%s.%03dZ"):
        super().__init__()
        self.fmt_dict = fmt_dict if fmt_dict is not None else {"message": "message"}
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None

    def usesTime(self) -> bool:
        return "asctime" in self.fmt_dict.values()

    def formatMessage(self, record) -> dict:
        return {fmt_key: record.__dict__[fmt_val] for fmt_key, fmt_val in self.fmt_dict.items()}

    def format(self, record) -> str:
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        message_dict = self.formatMessage(record)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            message_dict["exc_info"] = record.exc_text
        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)
        return json.dumps(message_dict, default=str)


def setup_logger() -> logging.Logger:
    json_handler = logging.StreamHandler()
    json_formatter = JsonFormatter({
        "level": "levelname",
        "ts": "asctime",
        "msg": "message",
        "name": "name",
    })
    json_handler.setFormatter(json_formatter)
    logging.getLogger().setLevel(logging.DEBUG)
    logger = logging.getLogger("telegram-bot")
    logger.addHandler(json_handler)
    return logger
