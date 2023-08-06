"""
Placeholder for future personal library
"""

from . import console
from . import path
from . import tts
from . import paste
from . import config
from . import custom_random
from ._version import get_versions
from . import custom_logging

__version__ = get_versions()['version']
del get_versions

MAIN_LOGGER = custom_logging.get_logger('ELIB')
MAIN_LOGGER.info(f'ELIB version {__version__}')
