"""CLI tool to list deployment histories."""

from argparse import ArgumentParser, Namespace

from functoolsplus import exiting
from his.pseudotypes import account
from hwdb.pseudotypes import deployment, system

from termgr.orm import DeploymentHistory


def get_args() -> Namespace:
    """Parses the command line arguments."""

    parser = ArgumentParser('Deployment history utility.')
    parser.add_argument(
        '-S', '--system', type=system,
        help='lists the deployment history of the given system')
    parser.add_argument(
        '-D', '--deployment', type=deployment,
        help='lists the deployment history of the given deployment')
    parser.add_argument(
        '-a', '--accounts', type=account, nargs='+',
        help='filters for deployments performed by the given accounts')
    parser.add_argument(
        '-d', '--desc', action='store_true', help='sort descending')
    return parser.parse_args()


@exiting
def main() -> int:
    """Runs the script and returns a returncode."""

    args = get_args()

    if args.deployment:
        condition = DeploymentHistory.new_deployment == args.deployment
    else:
        condition = DeploymentHistory.system == args.system

    if args.accounts:
        condition &= DeploymentHistory.account << args.accounts

    if args.desc:
        order = DeploymentHistory.timestamp.desc()
    else:
        order = DeploymentHistory.timestamp

    for record in DeploymentHistory.select().where(condition).order_by(order):
        print(record, flush=True)

    return 0
