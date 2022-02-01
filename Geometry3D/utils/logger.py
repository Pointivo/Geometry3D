"""Logger Module"""
import logging
from logging.config import dictConfig

main_logger = logging.getLogger()


def set_log_level(level='WARNING'):
    """
    **Input:**

    - level: a string of log level among 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.

        'WARNING' is the default.

    **Output:**

    No output but setup the log level for the logger
    """
    level=level.upper()
    global log_level, main_logger
    if level == 'DEBUG':
        log_level = logging.DEBUG
    elif level == 'INFO':
        log_level = logging.INFO
    elif level == 'WARNING':
        log_level = logging.WARNING
    elif level == 'ERROR':
        log_level = logging.ERROR
    elif level == 'CRITICAL':
        log_level = logging.CRITICAL
    else:
        raise ValueError("Unknown log level %s, which should one of 'DEBUG','INFO','WARNING','ERROR','CRITICAL'" % (log_level,))
    change_main_logger()


def change_main_logger():
    global main_logger, log_level
    main_logger = logging.getLogger()


def get_main_logger():
    '''
    **Input:**

    No Input

    **Output:**

    main_logger: The logger instance
    '''
    global main_logger
    return main_logger