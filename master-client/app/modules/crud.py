#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app import zession
from app.modules import http_client


def login(user, pswd, url="http://localhost:8080/api/login.php"):
    data = {"username": user, "pswd": pswd}
    data_rcv = http_client.json_post(url, data)
    if data_rcv and ("jwt" in data_rcv):
        return data_rcv["jwt"]
    return False


def read_data(data_type, filters=None):
    if filters is None:
        filters = {}
    url = "http://{}/api/get_{}.php".format(zession.remote_host, data_type)
    data = filters
    data['jwt'] = zession.token.jwt
    response = http_client.json_post(url, data=data)
    if response and (not 'message' in response):
        return response
    elif response and ('message' in response):
        return None
    else:
        return False


def update_data(data_type, new_data):
    url = "http://{}/api/update_{}.php".format(zession.remote_host, data_type)
    data = {'jwt': zession.token.jwt}

    if 'id' in new_data:
        data['id'] = new_data['id']

    if data_type == 'user':
        if not ('username' in new_data and 'pswd' in new_data):
            return False
        data['username'] = new_data['username']
        data['pswd'] = new_data['pswd']

    elif data_type == 'task':
        if 'manual_stop' in new_data:
            data['manual_stop'] = new_data['manual_stop']

    return http_client.json_post(url, data=data)


def create_data(data_type, data=None):
    if data is None:
        data = {}
    url = "http://{}/api/create_{}.php".format(zession.remote_host, data_type)
    data['jwt'] = zession.token.jwt
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
    return http_client.json_post(url, data=data)
