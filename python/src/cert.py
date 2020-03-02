from os import path
import requests

from config import SERVER_HOST

__all__ = ['create_certificate', 'init_certificate']


CERT_ENDPOINT: str = f'https://{SERVER_HOST}/cert'


def parent_dir(filename):
    """
    Fetch the filename from the parent directory of this file.
    :param filename: The filename to fetch
    """

    return path.join(path.dirname(__file__), '..', filename)


def create_certificate():
    """
    Create a certificate by requesting a new one from the server and writing to the root directory.
    """

    response = requests.post(CERT_ENDPOINT, verify=False)

    if response.status_code == 200:
        data = response.json()

        private_key = data['private']
        public_key = data['public']
        certificate = data['cert']

        with open(parent_dir('player.key'), 'w', encoding='utf-8') as f:
            f.write(private_key)
        with open(parent_dir('player.pub'), 'w', encoding='utf-8') as f:
            f.write(public_key)
        with open(parent_dir('player.crt'), 'w', encoding='utf-8') as f:
            f.write(certificate)


def init_certificate():
    """
    Initialize the player certificate by checking if it exists. If it does not,
    a new certificate will be fetched from the server before starting.
    """

    key = parent_dir('player.key')
    cert = parent_dir('player.crt')

    if not (path.exists(key) and path.exists(cert)):
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        create_certificate()

        print('Created player.key, player.pub and player.crt certificate files')
