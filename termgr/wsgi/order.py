"""API for terminal order submission."""

from his import authenticated, authorized

from termgr.orm import TerminalOrder
from termgr.wsgi.common import DATA


__all__ = ['ROUTES']


@authenticated
@authorized('terminal_order')
def order():
    """Submit a terminal order."""

    for order in DATA.json:
        order = TerminalOrder.from_dict(order)
        order.save()


ROUTES = (('POST', '/order', order, 'terminal_order'),)
