import os
import json
from subprocess import call, check_output
from sys import platform

HOME_DIR = os.path.expanduser('~')
AWS_DIR = HOME_DIR + '/.aws'
AWS_CONFIG = AWS_DIR + '/config'
AWS_CREDENTIALS = AWS_DIR + '/credentials'
ECS_DIR = HOME_DIR + '/.ecs'
ECS_CONFIG = ECS_DIR + '/config'
ECS_CREDENTIALS = ECS_DIR + '/credentials'

SECURITY_URL = 'https://console.aws.amazon.com/iam/home?region=us-east-1#'


def check_config_aws():
    return os.path.isdir(AWS_DIR) and os.path.isfile(AWS_CONFIG) and os.path.isfile(AWS_CREDENTIALS)


def check_config_ecs():
    return os.path.isdir(ECS_DIR) and os.path.isfile(ECS_CONFIG) and os.path.isfile(ECS_CREDENTIALS)


def read_default_aws_profile():
    lines = []
    with open(AWS_CREDENTIALS, 'r') as file:
        line = file.readline()
        while line:
            if '[' in line and ']' in line and 'default' not in line or line is '\n':
                break
            else:
                lines.append(line)
                line = file.readline()
    return lines


def set_profile_env_variables(profile='default'):
    if check_config_aws():
        environemnt_variables = {
            'AWS_ACCESS_KEY_ID': '',
            'AWS_SECRET_ACCESS_KEY': '',
            'AWS_SESSION_TOKEN': '',
            'AWS_MFA_SERIAL': ''
        }
        with open(AWS_CREDENTIALS) as file:
            line = file.readline()
            while line:
                vals = line.strip().replace(' ', '').split('=')
                if vals[0] == 'aws_access_key_id':
                    environemnt_variables['AWS_ACCESS_KEY_ID'] = vals[1]
                if vals[0] == 'aws_secret_access_key':
                    environemnt_variables['AWS_SECRET_ACCESS_KEY'] = vals[1]
                if vals[0] == 'aws_session_token':
                    environemnt_variables['AWS_SESSION_TOKEN'] = vals[1]
                if vals[0] == 'mfa_serial':
                    environemnt_variables['AWS_MFA_SERIAL'] = vals[1]

                if '[' in line and ']' in line and 'default' not in line or vals is '':
                    break
                line = file.readline()

        # if not call(['./awsac/env_vars']):
        for key, val in environemnt_variables.items():
            os.environ[key] = val
            # command = "export {}=\"{}\"".format(key, val)
            # call([command], shell=True)


def check_config(cli):
    check = False
    if cli is 'aws' or not cli:
        if not check_config_aws():
            return
    if cli is 'ecs' or not cli:
        if not check_config_ecs():
            return


def get_user():
    output = json.loads(check_output(
        ['aws', 'iam', 'get-user', '--profile', 'default']))
    return output['User']


def install_awscli(upgrade=False):
    devnull = open(os.devnull, 'w')
    if upgrade:
        c = call(["pip", "install", "awscli"], stdout=devnull)
    else:
        c = call(["pip", "install", "-U", "awscli"], stdout=devnull)

    if c and call(["aws", "--version"], stdout=devnull):
        print("Error installing awscli")
        raise SystemExit
    return True


def install_ecscli(upgrade=False,):
    devnull = open(os.devnull, 'w')
    if call(["which", "ecs-cli"], stdout=devnull) or (not call(["which", "ecs-cli"], stdout=devnull) and upgrade):
        url = 'https://s3.amazonaws.com/amazon-ecs-cli/'
        if platform == "linux" or platform == "linux2":
            url = '{}{}'.format(url, 'ecs-cli-linux-amd64-latest')
        elif platform == "darwin":
            url = '{}{}'.format(url, 'ecs-cli-darwin-amd64-latest')
        c = call(
            ['sudo', 'curl', '-o', '/usr/local/bin/ecs-cli', url], stdout=devnull)
        if c or (call(["sudo", "chmod", "+x", "/usr/local/bin/ecs-cli"]) and call(['ecs-cli', '--version'])):
            print("Error installing ecscli")
            raise SystemExit
    return True


def install_clis(*args, **kwargs):
    cli = kwargs.get('cli', None)
    upgrade = kwargs.get('upgrade', False)
    if cli is 'aws' or not cli:
        install_awscli(upgrade)
    if cli is 'ecs' or not cli:
        install_ecscli(upgrade)


def configure_awscli(user):
    if not check_config('aws'):
        devnull = open(os.devnull, 'w')
        security_url = SECURITY_URL
        instrucitons_url = 'https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html'
        if user:
            security_url = '{}/users/{}?section=security_credentials'.format(
                SECURITY_URL, user)
        for url in (instrucitons_url, security_url):
            call(["open", url])
        if not call(["pip", "show", "awscli"], stdout=devnull):
            call(["aws", "configure"])
    return True


def configure_ecscli():
    set_profile_env_variables()
    if not check_config('ecs'):
        devnull = open(os.devnull, 'w')
        if call(["ecs-cli", "configure", "profile", "--profile-name", 'default', '--access-key', os.environ['AWS_ACCESS_KEY_ID'], '--secret-key', os.environ['AWS_SECRET_ACCESS_KEY']], stdout=devnull):
            print("Error configuring ecscli")
            raise SystemExit


def configure_all(*args, **kwargs):
    user = kwargs.get('user', None)
    cli = kwargs.get('cli', None)
    if cli is 'aws' or not cli:
        configure_awscli(user)
    if cli is 'ecs' or not cli:
        configure_ecscli()


def update_aws_config(data):
    lines = read_default_aws_profile()
    lines.append('\n')
    lines.append('[mfa]\n')
    lines.append('output = json\n')
    lines.append('region = us-east-1\n')
    lines.append('aws_access_key_id = {}\n'.format(data['AccessKeyId']))
    lines.append('aws_secret_access_key = {}\n'.format(
        data['SecretAccessKey']))
    lines.append('aws_session_token = {}\n'.format(data['SessionToken']))

    with open(AWS_CREDENTIALS, 'w') as file:
        file.writelines(lines)


def get_mfa_serial(mfa_serial=None):
    set_profile_env_variables()
    if os.environ['AWS_MFA_SERIAL']:
        return os.environ['AWS_MFA_SERIAL']
    else:
        lines = read_default_aws_profile()
        if not mfa_serial:
            url = '{}/users/{}?section=security_credentials'.format(
                SECURITY_URL, get_user()['UserName'])
            call(["open", url])
            mfa_serial = input('MFA Device: ')
        mfa_serial_line = 'mfa_serial = {}\n'.format(mfa_serial)
        lines.append(mfa_serial_line)
        with open(AWS_CREDENTIALS, 'w') as file:
            file.writelines(lines)
        return mfa_serial


def get_mfa_session(**kwargs):
    token = kwargs.get('token', None)
    mfa_serial = kwargs.get('serial', None)

    serial_number = get_mfa_serial(mfa_serial)
    command = 'aws sts get-session-token --profile default --serial-number {} --token-code {}'.format(
        serial_number, token)
    output = json.loads(check_output([command], shell=True))
    update_aws_config(output['Credentials'])
