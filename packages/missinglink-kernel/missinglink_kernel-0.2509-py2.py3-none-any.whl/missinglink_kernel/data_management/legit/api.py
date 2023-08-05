# coding=utf-8
import logging
import requests

from six.moves.urllib import parse
from google.api_core import retry

from .config import get_prefix_section


BASE_URL_PATH = '_ah/api/missinglink/v1/'


def urljoin(*args):
    base = args[0]
    for u in args[1:]:
        base = parse.urljoin(base, u)

    return base


def handle_api(config, http_method, method_url, data=None):
    if config.id_token is None:
        logging.error('No id token for authentication')
        return

    url = urljoin(config.api_host, BASE_URL_PATH, method_url)

    id_token = config.id_token
    result = None
    for retries in range(3):
        headers = {'Authorization': 'Bearer {}'.format(id_token)}
        r = http_method(url, headers=headers, json=data)

        if r.status_code == 401:
            id_token = update_token(config)
            continue

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            try:
                error_message = ex.response.json().get('error', {}).get('message')
            except ValueError:
                error_message = str(ex)

            if error_message:
                logging.error(error_message)
                return

            raise

        result = r.json()
        break

    if result is None:
        logging.error('Failed to refresh the token')
        return

    return result


def build_auth0_url(auth0):
    return '{}.auth0.com'.format(auth0)


def _should_retry_auth0(exc):
    if not hasattr(exc, 'response'):
        return False

    error_codes_to_retries = [
        429,  # Too many requests
    ]
    return exc.response.status_code in error_codes_to_retries


@retry.Retry(predicate=_should_retry_auth0)
def update_token(config):
    r = requests.post('https://{}/delegation'.format(build_auth0_url(config.auth0)), json={
        'client_id': config.client_id,
        'grant_type': "urn:ietf:params:oauth:grant-type:jwt-bearer",
        'scope': 'openid offline_access user_external_id org orgs email picture name given_name user_metadata',
        'refresh_token': config.refresh_token,
    })

    r.raise_for_status()

    data = r.json()

    config.set(get_prefix_section(config.config_prefix, 'token'), 'id_token', data['id_token'])
    config.save()

    return data['id_token']
