#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.modules import http_client
from app.components import config, logger, token


def read_data(data_type, filters=None):
    if filters is None:
        filters = {}
    url = "{}/get_{}.php".format(config.credentials['cc_url'], data_type)
    data = filters
    data['jwt'] = token.jwt
    response = http_client.post_json(url, data=data)
    if response and (not 'message' in response):
        return response
    elif response and ('message' in response):
        return None
    else:
        return False


def update_data(data_type, new_data):
    url = "{}/update_{}.php".format(config.credentials['cc_url'], data_type)
    new_data["jwt"] = token.jwt
    response = http_client.post_json(url, data=new_data)
    if not (response and 'updated' in response['message']):
        logger.log('error trying to update {}'.format(data_type), 'ERROR')
        logger.log('new_data: {}'.format(data_type, new_data), 'DEBUG')
        return False
    return True


def create_data(data_type, data=None):
    if data is None:
        data = {}
    url = "{}/create_{}.php".format(config.credentials['cc_url'], data_type)
    data['jwt'] = token.jwt
    return http_client.post_json(url, data=data)