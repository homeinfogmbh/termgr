"""Terminal filtering"""

from datetime import datetime, timedelta

__all__ = ['deployed', 'online']


def deployed(terminals):
    """Filters only deployed terminals"""

    NULL = timedelta(0)

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
