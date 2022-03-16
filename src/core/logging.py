import os
import logging.config


def prepare_logging():
    os.makedirs("logs", exist_ok=True)
    logging.config.dictConfig(LOGGING)


LOGGING = dict()
