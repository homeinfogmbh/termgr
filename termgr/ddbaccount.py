"""Handling of a temporary DDB setup accounts."""

from argparse import ArgumentParser, Namespace
from typing import Iterable, Iterator

from his import Account, AccountService, CustomerService, Service, genpw
from hwdb import DeploymentType
from mdb import Customer, customer as customer_type
from termacls import GroupAdmin, TypeAdmin


__all__ = ['main']


DESCRIPTION = 'Manage temporary access to configure systems.'
EMAIL = 'ddbinstall@homeinfo.de'
FULL_NAME = 'DDB Setup Account'
GROUP = 1
TYPE = DeploymentType.DDB


def get_args() -> Namespace:
    """Return the command line arguments."""

    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        'customer', nargs='?', type=customer_type, help='the customer'
    )
    return parser.parse_args()


def print_accounts() -> None:
    """Print DDB setup accounts."""

    for account in list_accounts():
        print(account.name, account.customer)


def list_accounts() -> Iterable[Account]:
    """List DDB setup accounts."""

    return Account.select(cascade=True).where(
        Account.name << set(list_account_names())
    )


def list_account_names() -> Iterator[str]:
    """Yield names of potential DDB setup accounts."""

    for customer in Customer.select().where(True):
        yield get_account_name(customer)


def get_account_name(customer: Customer) -> str:
    """Return the DDB setup account name for the given customer."""

    return f'ddb-{customer.id}'


def get_account(customer: Customer) -> Account:
    """Update the image account."""

    name = get_account_name(customer.id)

    try:
        account = Account.get(Account.name == name)
    except Account.DoesNotExist:
        return Account(
            customer=customer,
            email=EMAIL,
            full_name=FULL_NAME,
            name=name
        )

    account.customer = customer
    return account


def get_service(name: str) -> Service:
    """Get a service by its name."""

    return Service.get(Service.name == name)


def enable_account_service(
        account: Account,
        service: Service
) -> AccountService:
    """Enable the account for the given service."""

    try:
        return AccountService.get(
            (AccountService.account == account)
            & (AccountService.service == service)
        )
    except AccountService.DoesNotExist:
        account_service = AccountService(account=account, service=service)
        account_service.save()
        return account_service


def enable_customer_service(
        customer: Customer,
        service: Service
) -> CustomerService:
    """Enable the customer for the given service."""

    try:
        return CustomerService.get(
            (CustomerService.customer == customer)
            & (CustomerService.service == service)
        )
    except CustomerService.DoesNotExist:
        customer_service = CustomerService(customer=customer, service=service)
        customer_service.save()
        return customer_service


def disable_customer_service(customer: Customer, service: Service) -> None:
    """Disable the customer for the given service."""

    for customer_service in CustomerService.select().where(
            (CustomerService.customer == customer)
            & (CustomerService.service == service)
    ):
        customer_service.delete_instance()


def enable_group_admin(account: Account, group: int) -> GroupAdmin:
    """Enable the account as admin for the given group."""

    try:
        return GroupAdmin.get(
            (GroupAdmin.account == account) & (GroupAdmin.group == group)
        )
    except GroupAdmin.DoesNotExist:
        group_admin = GroupAdmin(account=account, group=group)
        group_admin.save()
        return group_admin


def enable_type_admin(account: Account, typ: DeploymentType) -> TypeAdmin:
    """Enable the account as admin for the given type."""

    try:
        return TypeAdmin.get(
            (TypeAdmin.account == account) & (TypeAdmin.type == typ)
        )
    except TypeAdmin.DoesNotExist:
        type_admin = TypeAdmin(account=account, type=typ)
        type_admin.save()
        return type_admin


def enable_account(account: Account) -> None:
    """Update and print the account data."""

    account.disabled = False
    account.failed_logins = 0
    account.passwd = passwd = genpw(length=8)
    account.save()
    enable_account_service(account, termgr := get_service('termgr'))
    enable_customer_service(account.customer, termgr)
    enable_group_admin(account, GROUP)
    enable_type_admin(account, TYPE)
    print('Customer:', account.customer)
    print('Account: ', account.name)
    print('Password:', passwd)


def disable_account(account: Account) -> None:
    """Disables the account."""

    disable_customer_service(account.customer, get_service('termgr'))
    account.delete_instance()
    print('Account', f'"{account.name}"', 'deleted.')


def toggle_account(account: Account) -> None:
    """Toggle the account."""

    if account.id is None or account.disabled:
        return enable_account(account)

    return disable_account(account)


def main() -> int:
    """Run the program."""

    args = get_args()

    if args.customer is None:
        print_accounts()
    else:
        toggle_account(get_account(args.customer))

    return 0
