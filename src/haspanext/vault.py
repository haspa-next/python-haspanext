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
        creds.access_key, creds.secret_key, creds.token, role='service-%-%-iam' % (service, env), header_value='vault.it.paulalex.de'
    ))

    print('Downloading vault secrets')
    globals.config = vault.secrets.kv.v1.read_secret(
        path = 'service/%/%' % (service, env)
    )['data']
    print('Secrets obtained')
    print('The service name is {name}'.format(
        name = globals.config['name']
    ))
