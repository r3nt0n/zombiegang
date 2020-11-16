#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import json

from app import zession
from app.modules import http_client


def read_data(data_type, filters=None):
    if filters is None:
        filters = {}
    url = "http://{}/api/get_{}.php".format(zession.remote_host, data_type)
    data = filters
    data['jwt'] = zession.token.jwt
    data = json.dumps(data)
    # print(data)
    return http_client.json_post(url, data=data)


def update_data(data_type, new_data):
    url = "http://{}/api/update_{}.php".format(zession.remote_host, data_type)
    data = {'jwt': zession.token.jwt}

    if data_type == 'user':
        if not ('username' in new_data and 'pswd' in new_data):
            return False
        data['username'] = new_data['username']
        data['pswd'] = new_data['pswd']

    data = json.dumps(data)
    return http_client.json_post(url, data=data)


def create_data(data_type, data=None):
    if data is None:
        data = {}
    url = "http://{}/api/create_{}.php".format(zession.remote_host, data_type)
    data['jwt'] = zession.token.jwt
    data = json.dumps(data)
    return http_client.json_post(url, data=data)


def delete_data(data_type, data_id):
    url = "http://{}/api/delete_{}.php".format(zession.remote_host, data_type)
    data = {'jwt': zession.token.jwt}
    if not (data_id):
        return False
    if (data_type == 'user' or data_type == 'master' or data_type == 'zombie'):
        data['username'] = data_id
    else:
        data['id'] = data_id
    data = json.dumps(data)
    return http_client.json_post(url, data=data)