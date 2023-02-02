import logging
import sys

import const


def set_logger():
    logger = logging.getLogger(const.LOGGER_NAME)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter('%(levelname)s %(message)s')
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        file_handler = logging.FileHandler(
                'errors.log', encoding='utf-8', mode='w')
        file_formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.ERROR)
        logger.addHandler(file_handler)
    return logger
