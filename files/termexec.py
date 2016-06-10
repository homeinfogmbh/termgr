"""Terminal checker

Usage:
    termexec <cmd> <expr>... [options]

Options:
    --help          Show this page.
"""
from contextlib import suppress

from docopt import docopt

from homeinfo.terminals.filter import TerminalFilter
from homeinfo.terminals.ctrl import RemoteController


USER = 'termgr'
options = docopt(__doc__)

for expr in options['<expr>']:
    for terminal in TerminalFilter(expr):
        rc = RemoteController(USER, terminal)
        result = rc.execute(options['<cmd>'])

        if result:
            with suppress(AttributeError):
                print(result.stdout.decode())

            exit(0)
        else:
            with suppress(AttributeError):
                print(result.sterr.decode())

            exit(2)
