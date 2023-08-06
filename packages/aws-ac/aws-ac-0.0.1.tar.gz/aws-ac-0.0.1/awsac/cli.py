import click
import sys
from awsac.core import install_clis, configure_all, get_mfa_session


@click.group()
def cli():
    """awc-ac
    Automatically configurate credentials for AWS and ECS cli's
    """
    if sys.version_info[0] == 2:
        print("Current environment is Python 2.")
        print("Please use a Python 3.6 virtualenv.")
        raise SystemExit


@cli.command('install')
@click.option('--upgrade', is_flag=True)
@click.argument('cli', required=False)
def install(upgrade, cli):
    kwargs = {'upgrade': upgrade, 'cli': cli}
    install_clis(**kwargs)


@cli.command('configure')
@click.argument('user', required=False)
@click.argument('cli', required=False)
def configure(user, cli):
    kwargs = {'user': user, 'cli': cli}
    configure_all(**kwargs)


@cli.command('mfa')
@click.argument('token')
@click.argument('serial', required=False)
def mfa(token, serial):
    kwargs = {'token': token, 'serial': serial}
    get_mfa_session(**kwargs)


def main():
    cli()


if __name__ == '__main__':
    main()
