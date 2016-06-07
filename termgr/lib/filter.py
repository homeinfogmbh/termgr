"""Terminal filtering"""

from datetime import datetime, timedelta
from logging import getLogger

__all__ = ['deployed', 'online']


def deployed(terminals, logger=None):
    """Filters only deployed terminals"""

    NAME = 'Deployment filter'
    NULL = timedelta(0)

    if logger is None:
        logger = getLogger(NAME)
    else:
        logger = logger.getChild(NAME)

    for terminal in terminals:
        if terminal.deployed is None:
            logger.warning('Terminal {0} is not deployed'.format(terminal))
        elif terminal.deployed - datetime.now() > NULL:
            logger.warning('Terminal {0} is not yet deployed'.format(terminal))
        else:
            yield terminal


def online(terminals):
    """Yields terminals that are online"""

    for terminal in terminals:
        if terminal.status:
            yield terminal
