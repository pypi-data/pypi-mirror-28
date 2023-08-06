# AWS AC: Auto Credentials

```
pip install aws-ac
aws-ac start
```

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

### aws-ac start [OPTIONS] 
```
Options:
  --user TEXT    AWS Username
  --token TEXT   MFA Token
  --serial TEXT  MFA Serial
```

### aws-ac install [OPTIONS]
This installs the [aws-cli](https://aws.amazon.com/documentation/cli/) and [ecs-cli](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI.html) tools.
Supplying the `--upgrade` flag will update or reinstall the cli's to their newest verisons.
```
Options:
  --upgrade
  --cli TEXT  CLI
```

### aws-ac configure [OPTIONS]
This prompts the user to configure the aws and ecs profiles. By providing the argument CLI with 'aws' or 'ecs' it can configure only one.

```
Options:
  --user TEXT  AWS Username
  --cli TEXT   CLI
```

### aws-ac mfa [OPTIONS] TOKEN
This prompts the user to obtain their mfa_serial key and if it has already been added creates a aws profile with a valid session token.
```
Options:
  --serial TEXT  MFA Serial
```


