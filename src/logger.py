import logging
import logging.config
import os

_here = os.path.split(os.path.abspath(__file__))[0]
logging.config.fileConfig(os.path.join(_here, 'config', 'logging.ini'))


def get_logger(name):

    ''' Get a logger with the given name '''

    return logging.getLogger(name)
