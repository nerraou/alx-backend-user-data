#!/usr/bin/env python3
"""
handling Personal Data
"""
import re
from typing import List
import logging


PII_FIELDS = ("name",
              "email",
              "phone",
              "password",
              "ip",
              )


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ function that returns the log message obfuscated:"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """create user data logger"""
    logger = logging.Logger("user_data", logging.INFO)
    logger.addHandler(RedactingFormatter(fields=PII_FIELDS))

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using filter_datum """
        message = super().format(record)
        return filter_datum(self.__fields,
                            self.REDACTION, message, self.SEPARATOR)
