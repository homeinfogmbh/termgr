"""List systems."""

from his import ACCOUNT, authenticated, authorized
from hwdb import Deployment, System
from mdb import Address, Company, Customer
from wsgilib import JSON

from flask import Response
from peewee import JOIN, ModelSelect

from termacls import get_deployment_admin_condition, get_system_admin_condition


__all__ = ['ROUTES']


def _get_deployments() -> ModelSelect:
    """Returns the respective deployments."""

    lpt_address = Address.alias()
    return Deployment.select(
        Deployment, Customer, Company, Address, lpt_address
    ).join_from(
        Deployment, Customer, on=Deployment.customer == Customer.id,
        join_type=JOIN.LEFT_OUTER
    ).join_from(
        Customer, Company, on=Customer.company == Company.id,
        join_type=JOIN.LEFT_OUTER
    ).join_from(
        Deployment, Address, on=Deployment.address == Address.id,
        join_type=JOIN.LEFT_OUTER
    ).join_from(
        Deployment, lpt_address,
        on=Deployment.lpt_address == lpt_address.id,
        join_type=JOIN.LEFT_OUTER
    ).where(
        get_deployment_admin_condition(ACCOUNT)
    )


def _get_systems() -> ModelSelect:
    """Returns the respective systems."""

    lpt_address = Address.alias()
    dataset = Deployment.alias()
    dataset_address = Address.alias()
    dataset_lpt_address = Address.alias()
    return System.select(
        System, Deployment, Address, Customer, Company, lpt_address, dataset,
        dataset_address, dataset_lpt_address
    ).join_from(
        System, Deployment, on=System.deployment == Deployment.id,
        join_type=JOIN.LEFT_OUTER
    ).join_from(
        Deployment, Customer, on=Deployment.customer == Customer.id,
        join_type=JOIN.LEFT_OUTER
    ).join_from(
        Customer, Company, on=Customer.company == Company.id,
        join_type=JOIN.LEFT_OUTER
    ).join_from(
        Deployment, Address, on=Deployment.address == Address.id,
        join_type=JOIN.LEFT_OUTER
    ).join_from(
        Deployment, lpt_address, on=Deployment.lpt_address == lpt_address.id,
        join_type=JOIN.LEFT_OUTER
    ).join_from(
        System, dataset, on=System.dataset == dataset.id,
        join_type=JOIN.LEFT_OUTER
    ).join_from(
        dataset, dataset_address, on=dataset.address == dataset_address.id,
        join_type=JOIN.LEFT_OUTER
    ).join_from(
        dataset, dataset_lpt_address,
        on=dataset.lpt_address == dataset_lpt_address.id,
        join_type=JOIN.LEFT_OUTER
    ).where(
        get_system_admin_condition(ACCOUNT)
    )


@authenticated
@authorized('termgr')
def list_deployments() -> Response:
    """Lists available deployments."""

    return JSON([
        dep.to_json(systems=True, cascade=2) for dep in _get_deployments()
    ])


@authenticated
@authorized('termgr')
def get_system(ident: int) -> Response:
    """Lists the available systems."""

    systems = _get_systems().where(System.id == ident)

    try:
        system = systems.get()
    except System.DoesNotExist:
        return ('No such system.', 404)

    return JSON(system.to_json(cascade=3, brief=True))


@authenticated
@authorized('termgr')
def list_systems() -> Response:
    """Lists the available systems."""

    return JSON([sys.to_json(cascade=3, brief=True) for sys in _get_systems()])


ROUTES = (
    ('GET', '/list/deployments', list_deployments),
    ('GET', '/list/systems/<int:ident>', get_system),
    ('GET', '/list/systems', list_systems)
)
