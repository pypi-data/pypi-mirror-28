# coding=utf-8
"""
Utilities to control the console window
"""

import ctypes

import elib.custom_logging

LOGGER = elib.custom_logging.get_logger('ELIB').getChild(__name__)


def set_title(title: str):
    """
    Sets the console title

    Args:
        title: title as a string
    """
    LOGGER.debug(f'setting console title to {title}')
    ctypes.windll.kernel32.SetConsoleTitleW(title)
