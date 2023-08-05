import requests_unixsocket
import json
import os
from connection import request


def get_app_dir(app):
    return request('/app/install_path?name={0}'.format(app))


def get_data_dir(app):
    return request('/app/data_path?name={0}'.format(app))


