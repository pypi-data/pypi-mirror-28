# AWS AC: Auto Credentials

## Install
Must be using Python 3! For MacOS and Linux. No native Windows support.
```
pip install aws-ac
```

If Python 3 is not your default Python Environment:
```
python3 -m venv venv
source venv/bin/activate
pip install aws-ac
```

## Commands

### aws-ac install [--upgrade]
This installs the [aws-cli](https://aws.amazon.com/documentation/cli/) and [ecs-cli](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI.html) tools.
Supplying the `--upgrade` flag will update or reinstall the cli's to their newest verisons.
```
aws-ac

aws-ac --upgrade
```

### aws-ac configure [USER] [CLI]
This prompts the user to configure the aws and ecs profiles. By providing the argument CLI with 'aws' or 'ecs' it can configure only one.
```
aws-ac configure

aws-ac configure aws

aws-ac configure ecs
```

### aws-ac mfa \<TOKEN\> [SERIAL]
This prompts the user to obtain their mfa_serial key and if it has already been added creates a aws profile with a valid session token.
```
aws-ac mfa 123456

aws-ac mfa 123456 <mfa_serial>
```
