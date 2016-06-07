"""Text user interface for termgr"""

__all__ = ['printterm']


def printterm(terminal, process_result):
    """Prints a process result"""

    try:
        msg = process_result.stdout.decode().strip()
    except (TypeError, ValueError, AttributeError):
        msg = process_result.stdout

    print(terminal, msg, sep=': ')
