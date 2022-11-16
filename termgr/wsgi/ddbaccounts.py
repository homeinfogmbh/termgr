"""Manage temporary DDB setup accounts."""

from flask import request

from his import Account, authenticated, authorized, root
from mdb import Customer
from wsgilib import JSON, JSONMessage

from termgr.ddbaccount import disable_account
from termgr.ddbaccount import enable_account
from termgr.ddbaccount import get_account
from termgr.ddbaccount import list_accounts


__all__ = ['ROUTES']


def get_account_from_json() -> Account:
    """Returns the requested account from the JSON data."""

    if (cid := request.json.get('customer')) is None:
        raise JSONMessage('No customer specified', status=400)

    try:
        customer = Customer.get(cid)
    except (ValueError, TypeError):
        raise JSONMessage('invalid customer ID', status=400)
    except Customer.DoesNotExist:
        raise JSONMessage('No such customer', status=404)

    return get_account(customer)


@authenticated
@authorized('termgr')
@root
def _list_accounts() -> JSON:
    """List temporary setup accounts."""

    return JSON([account.to_json() for account in list_accounts()])


@authenticated
@authorized('termgr')
@root
def _enable_account() -> JSON:
    """Enables / adds a temporary setup accounts."""

    passwd = enable_account(account := get_account_from_json())
    return JSON({**account.to_json, 'passwd': passwd})


@authenticated
@authorized('termgr')
@root
def _disable_account() -> JSONMessage:
    """Removes a temporary setup account."""

    disable_account(get_account_from_json())
    return JSONMessage('Account deleted.')


ROUTES = [
    ('GET', '/ddbaccount/list', _list_accounts),
    ('POST', '/ddbaccount/enable', _enable_account),
    ('POST', '/ddbaccount/disable', _disable_account)
]
