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


@cli.command('start')
@click.option('--user', default=None, help='AWS Username', required=False)
@click.option('--token', default=None, help='MFA Token', required=False)
@click.option('--serial', default=None, help='MFA Serial', required=False)
def start(user, token, serial):
    kwargs = {
        'user': user,
        'token': token,
        'serial': serial
    }
    install_clis(**kwargs)
    configure_all(**kwargs)
    if token:
        get_mfa_session(**kwargs)


@cli.command('install')
@click.option('--upgrade', is_flag=True)
@click.option('--cli', default=None, help='CLI', required=False)
def install(upgrade, cli):
    kwargs = {'upgrade': upgrade, 'cli': cli}
    install_clis(**kwargs)


@cli.command('configure')
@click.option('--user', default=None, help='AWS Username', required=False)
@click.option('--cli', default=None, help='CLI', required=False)
def configure(user, cli):
    kwargs = {'user': user, 'cli': cli}
    configure_all(**kwargs)


@cli.command('mfa')
@click.argument('token')
@click.option('--serial', default=None, help='MFA Serial', required=False)
def mfa(token, serial):
    kwargs = {'token': token, 'serial': serial}
    get_mfa_session(**kwargs)


def main():
    cli()


if __name__ == '__main__':
    main()
