"""Handling of a temporary DDB setup accounts."""

from argparse import ArgumentParser, Namespace

from his import Account, AccountService, CustomerService, Service, genpw
from hwdb import DeploymentType
from mdb import Customer, customer
from termacls import GroupAdmin, TypeAdmin


__all__ = ['main']


DESCRIPTION = 'Manage temporary access to configure systems.'
GROUP = 1
NAME = 'ddbinstall'
TYPE = DeploymentType.DDB


def get_args() -> Namespace:
    """Return the command line arguments."""

    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument('customer', type=customer, help='the customer')
    return parser.parse_args()


def get_account(customer: Customer) -> Account:
    """Update the image account."""

    try:
        return Account.select(cascade=True).where(
            (Account.name == NAME) & (Account.customer == customer)
        ).get()
    except Account.DoesNotExist:
        return Account(name=NAME, customer=customer)


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


def disable_account_service(account: Account, service: Service) -> None:
    """Disable the account for the given service."""

    for account_service in AccountService.select().where(
            (AccountService.account == account)
            & (AccountService.service == service)
    ):
        account_service.delete_instance()


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


def enable_type_admin(account: Account, type: DeploymentType) -> TypeAdmin:
    """Enable the account as admin for the given type."""

    try:
        return TypeAdmin.get(
            (TypeAdmin.account == account) & (TypeAdmin.type == type)
        )
    except TypeAdmin.DoesNotExist:
        type_admin = TypeAdmin(account=account, type=type)
        type_admin.save()
        return type_admin


def disable_group_admin(account: Account, group: int) -> None:
    """Disable the account as admin for the given group."""

    for group_admin in GroupAdmin.select().where(
            (GroupAdmin.account == account) & (GroupAdmin.group == group)
    ):
        group_admin.delete_instance()


def disable_type_admin(account: Account, type: DeploymentType) -> None:
    """Disable the account as admin for the given type."""

    for type_admin in TypeAdmin.select().where(
            (TypeAdmin.account == account) & (TypeAdmin.type == type)
    ):
        type_admin.delete_instance()


def enable_account(account: Account) -> None:
    """Update and print the account data."""

    account.disabled = False
    account.failed_logins = 0
    account.passwd = passwd = genpw()
    account.save()
    enable_account_service(account, termgr := get_service('termgr'))
    enable_customer_service(account.customer, termgr)
    enable_group_admin(account, GROUP)
    enable_type_admin(account, TYPE)
    print('Account: ', account.name)
    print('Customer:', account.customer)
    print('Password:', passwd)


def disable_account(account: Account) -> None:
    """Disables the account."""

    account.disabled = True
    account.save()
    disable_account_service(account, termgr := get_service('termgr'))
    disable_customer_service(account.customer, termgr)
    disable_group_admin(account, GROUP)
    disable_type_admin(account, TYPE)


def toggle_account(account: Account) -> None:
    """Toggle the account."""

    if account.id is None or account.disabled:
        return enable_account(account)

    return disable_account(account)


def main() -> int:
    """Run the program."""

    args = get_args()
    toggle_account(get_account(args.customer))
    return 0
