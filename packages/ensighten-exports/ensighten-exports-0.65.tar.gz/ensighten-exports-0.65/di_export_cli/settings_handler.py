import os
import urllib3
import yaml
import base64
from swagger.swagger_client.configuration import Configuration
from httprequests import HttpRequest
from requests import HTTPError
import re


def update_auth_token(credentials):
    url = get_api_url(credentials)
    username = credentials['account'] + '+' + credentials['username']
    password = base64.b64decode(credentials['password'])
    # make call to auth with username and pw, then get header and put in api key
    response = HttpRequest(url).get_auth_token(username, password)
    Configuration().api_key['api_key'] = response.headers['x-auth-token']


def get_api_url(credentials):
    try:
        return credentials['url'].strip('/')
    except KeyError:
        # Default
        return 'https://api.data.ensighten.com'


def update_configuration(http_headers=None):
    try:
        Configuration().headers = get_header_dict(http_headers)
    except ValueError as e:
        print e.message
        return False
    credentials = get_credentials()
    Configuration().host = get_api_url(credentials)
    if 'username' not in credentials:
        print "Username is missing, please run configure"
        return False
    if 'password' not in credentials:
        print "Password is missing, please run configure"
        return False
    try:
        update_auth_token(credentials)
        return True
    except HTTPError as e:
        if e.response.status_code == 401:
            print 'Credentials invalid'
        else:
            print 'Error while validating credentials'
            raise
        return False
    except urllib3.exceptions.MaxRetryError:
        print 'Could not establish connection'
        return False
    except Exception:
        print 'Could not validate credentials'
        raise


# Parse input http headers into dictionary and validate that it has correct format.
def get_header_dict(http_headers):
    headers = {}
    if http_headers is None:
        return headers;

    for header in http_headers:
        regex = re.compile(ur'(.+?)=(.+?)$')
        regexed_header = re.search(regex, header)
        if regexed_header is None:
            raise ValueError('Could not parse http_header, make sure it looks like <key>=<value>')
        headers[str(regexed_header.group(1))] = str(regexed_header.group(2))
    return headers


def store_credentials(account, username, password):
    credentials = {'account': account, 'username': username, 'password': base64.b64encode(password)}
    with open(get_credentials_file_path(), 'w') as credentials_file:
        credentials_file.write(yaml.safe_dump(credentials, default_flow_style=False))


def get_credentials():
    if os.path.isfile(get_credentials_file_path()):
        with open(get_credentials_file_path(), 'r') as credentials_file:
            return yaml.load(credentials_file)
    else:
        return {}


def get_credentials_file_path():
    file_name = 'credentials.yml'
    home = os.path.expanduser("~")
    ensighten_directory = os.path.join(home, '.ensighten')
    if not os.path.isdir(ensighten_directory):
        os.makedirs(ensighten_directory)
    return os.path.join(ensighten_directory, file_name)

