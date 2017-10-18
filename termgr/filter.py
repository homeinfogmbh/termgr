"""Terminal filtering."""

from datetime import datetime, timedelta

__all__ = ['deployed', 'online']


def deployed(terminals, logger=None):
    """Yields deployed terminals."""

    for terminal in terminals:
        if terminal.deployed is None:
            if logger is not None:
                logger.warning('Terminal {} is not deployed.'.format(terminal))
        elif terminal.deployed - datetime.now() > timedelta(0):
            if logger is not None:
                logger.warning('Terminal {} is not yet deployed.'.format(
                    terminal))
        else:
            yield terminal


def online(terminals, logger=None):
    """Yields terminals that are online."""

    for terminal in terminals:
        if terminal.status:
            yield terminal
        elif logger is not None:
            logger.warning('Terminal {} is offline'.format(terminal))
