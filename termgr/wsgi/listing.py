"""List systems."""

from typing import Iterable, Union

from his import ACCOUNT, Account, authenticated, authorized
from hwdb import Deployment, System
from mdb import Address, Company, Customer
from wsgilib import JSON, JSONMessage

from peewee import JOIN, ModelSelect, prefetch

from termacls import get_deployment_admin_condition, get_system_admin_condition


__all__ = ["ROUTES"]


def _get_deployments(account: Account) -> Iterable[Deployment]:
    """Returns the respective deployments."""

    lpt_address = Address.alias()
    deployments = (
        Deployment.select(Deployment, Customer, Company, Address, lpt_address)
        .join_from(
            Deployment,
            Customer,
            on=Deployment.customer == Customer.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .join_from(
            Customer,
            Company,
            on=Customer.company == Company.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .join_from(
            Deployment,
            Address,
            on=Deployment.address == Address.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .join_from(
            Deployment,
            lpt_address,
            on=Deployment.lpt_address == lpt_address.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .where(get_deployment_admin_condition(account))
    )
    return prefetch(deployments, System.select())


def _get_systems(account: Account) -> ModelSelect:
    """Returns the respective systems."""

    lpt_address = Address.alias()
    dataset = Deployment.alias()
    dataset_address = Address.alias()
    dataset_lpt_address = Address.alias()
    return (
        System.select(
            System,
            Deployment,
            Address,
            Customer,
            Company,
            lpt_address,
            dataset,
            dataset_address,
            dataset_lpt_address,
        )
        .join_from(
            System,
            Deployment,
            on=System.deployment == Deployment.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .join_from(
            Deployment,
            Customer,
            on=Deployment.customer == Customer.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .join_from(
            Customer,
            Company,
            on=Customer.company == Company.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .join_from(
            Deployment,
            Address,
            on=Deployment.address == Address.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .join_from(
            Deployment,
            lpt_address,
            on=Deployment.lpt_address == lpt_address.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .join_from(
            System, dataset, on=System.dataset == dataset.id, join_type=JOIN.LEFT_OUTER
        )
        .join_from(
            dataset,
            dataset_address,
            on=dataset.address == dataset_address.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .join_from(
            dataset,
            dataset_lpt_address,
            on=dataset.lpt_address == dataset_lpt_address.id,
            join_type=JOIN.LEFT_OUTER,
        )
        .where(get_system_admin_condition(account))
    )


@authenticated
@authorized("termgr")
def list_deployments() -> JSON:
    """Lists available deployments."""

    return JSON(
        [
            deployment.to_json(systems=True, cascade=2)
            for deployment in _get_deployments(ACCOUNT)
        ]
    )


@authenticated
@authorized("termgr")
def get_system(ident: int) -> Union[JSONMessage, JSON]:
    """Lists the available systems."""

    systems = _get_systems(ACCOUNT).where(System.id == ident)

    try:
        system = systems.get()
    except System.DoesNotExist:
        return JSONMessage("No such system.", status=404)

    return JSON(system.to_json(cascade=3, brief=True))


@authenticated
@authorized("termgr")
def list_systems() -> JSON:
    """Lists the available systems."""

    return JSON(
        [system.to_json(cascade=3, brief=True) for system in _get_systems(ACCOUNT)]
    )


ROUTES = [
    ("GET", "/list/deployments", list_deployments),
    ("GET", "/list/systems/<int:ident>", get_system),
    ("GET", "/list/systems", list_systems),
]
