import requests_unixsocket
import json
import os
from connection import request


def get_app_url(app):
    return request('/app/url?name={0}'.format(app))
