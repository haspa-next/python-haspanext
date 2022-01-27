import os
import sys
import hvac
import boto3

def obtain_config(service, env):
    print('Obtaining vault configuration')
    vault = hvac.Client(
        url = 'https://vault.it.paulalex.de'
    )

    creds = boto3.Session().get_credentials()
    print('Login via IAM')
    print(vault.auth.aws.iam_login(
        creds.access_key, creds.secret_key, creds.token, role='service-%s-%s-iam' % (service, env), header_value='vault.it.paulalex.de'
    ))

    print('Downloading vault secrets')
    config = vault.secrets.kv.v1.read_secret(
        path = 'service/%s/%s' % (service, env)
    )['data']
    print('Secrets obtained')
    print('The service name is {name}'.format(
        name = config['name']
    ))
    for key, value in config.items():
        os.environ[key] = value.upper()

