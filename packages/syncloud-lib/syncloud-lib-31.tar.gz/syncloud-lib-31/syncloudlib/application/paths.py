import requests_unixsocket
import json
import os

socket_file = '/opt/data/platform/api.socket'.replace('/', '%2F')
socket = 'http+unix://{0}'.format(socket_file)


def get_app_dir(app):
    return _query('/app/install_path?name={0}'.format(app))


def get_data_dir(app):
    return _query('/app/data_path?name={0}'.format(app))


def _query(url):
    session = requests_unixsocket.Session()
    try:
        response = session.get('{0}{1}'.format(socket, url))
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if 'success' in response_json and response_json['success']:
                return response_json['data']
            else:
                raise Exception('service error: {0}'.format(response_json['message']))
            
        else:
            raise Exception('unablento connect to {0} with error code: {1}'.format(socket, response.stats_code))
    except Exception, e:
        raise Exception('unable to connect to {0}'.format(socket), e)