"""API for terminal order submission."""

from his import ACCOUNT, CUSTOMER, authenticated, authorized, Account
from mdb import Customer
from wsgilib import Error, JSON

from termgr.orm import TerminalOrder
from termgr.wsgi.common import DATA


__all__ = ['ROUTES']


def get_orders():
    """Returns the respective order."""

    if ACCOUNT.root:
        return TerminalOrder

    if ACCOUNT.admin:
        TerminalOrder.select().join(Account).join(
            Customer, on=(Customer.id == Account.customer)).select().where(
                Customer == CUSTOMER.id)

    return TerminalOrder.select().where(TerminalOrder.account == ACCOUNT.id)


def get_order(ident):
    """Returns the respective order."""

    try:
        return TerminalOrder.get(
            (TerminalOrder.id == ident)
            & (TerminalOrder.customer == ACCOUNT.id))
    except TerminalOrder.DoesNotExist:
        raise Error('No such order.', status=404)


@authenticated
@authorized('terminal_order')
def list_():
    """Lists terminal orders."""

    return JSON([order.to_dict() for order in get_orders()])


@authenticated
@authorized('terminal_order')
def submit_order():
    """Submit a terminal order."""

    for order in DATA.json:
        order = TerminalOrder.from_dict(CUSTOMER.id, order)
        order.save()

    return ('Orders added.', 201)


@authenticated
@authorized('terminal_order')
def cancel_order(ident):
    """Cancel a terminal order."""

    get_order(ident).delete_instance()
    return 'Order deleted.'


ROUTES = (
    ('GET', '/order', list_, 'list_orders'),
    ('POST', '/order', submit_order, 'submit_order'),
    ('DELETE', '/order/<int:ident>', cancel_order, 'cancel_order'))
