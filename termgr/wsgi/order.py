"""API for terminal order submission."""

from his import authenticated, authorized

from termgr.orm import TerminalOrder
from termgr.wsgi.common import DATA


@authenticated
@authorized('terminal_order')
def order():
    """Submit a terminal order."""

    for order in DATA.json:
        order = TerminalOrder.from_dict(order)
        order.save()
