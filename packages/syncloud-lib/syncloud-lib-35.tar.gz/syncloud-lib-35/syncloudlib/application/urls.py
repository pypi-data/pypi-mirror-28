from connection import request


def get_app_url(app):
    return request('/app/url?name={0}'.format(app))
