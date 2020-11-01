#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import requests, json


def get_data(data_type, zession, by_username=False, by_datetime_bef=False, by_datetime_aft=False, by_os=False):
    data = { 'jwt': zession.jwt }
    if by_username:
        data['username'] = by_username
    if by_datetime_bef:
        data['datetime_bef'] = by_datetime_bef
    if by_datetime_aft:
        data['datetime_aft'] = by_datetime_aft
    if by_os:
        data['os'] = by_os
    data = json.dumps(data)
    #print(data)
    r = requests.post("http://{}/api/get_{}.php".format(zession.remote_hostname, data_type), data=data)
    if r.status_code != 200:
        return False
    return json.loads(r.content.decode('utf-8-sig'))



def get_filtered_data(zession, request, data_type, by_username='', by_datetime_bef='', by_datetime_aft='', by_os=''):
    #print(request.form)
    if (request.method == 'POST') and ('btn-filter' in request.form):
        #print('filter-checkpoint')
        try:
            by_username = request.form.get('username')
            by_os = request.form.get('os_filter')
            by_datetime_bef = ((request.form.get('date_bef_filter') + ' ' + request.form.get('time_bef_filter')).rstrip()).lstrip()
            by_datetime_aft = ((request.form.get('date_aft_filter') + ' ' + request.form.get('time_aft_filter')).rstrip()).lstrip()
        except TypeError:
            pass

    return get_data(data_type, zession, by_username, by_datetime_bef, by_datetime_aft, by_os)