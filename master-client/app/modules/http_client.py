#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import json
from app import proxy

def post(url, data):
    from app import logger
    r = proxy.session.post(url, data=data)
    logger.log('url: {}'.format(url), level='DEBUG')
    logger.log('data sent: {}'.format(data), level='DEBUG')
    if r.status_code == 202:
        data_rcv = None
        logger.log('any content received', level='WARNING')
    elif r.status_code != 200:
        data_rcv = False
        logger.log('{} http code received'.format(r.status_code), level='ERROR')
        logger.log('url: {}'.format(url), level='DEBUG')
        logger.log('data sent: {}'.format(data), level='DEBUG')
    else:
        data_rcv = r.content.decode('utf-8-sig')
        logger.log('{} http code received'.format(r.status_code), level='DEBUG')
    return data_rcv


def json_post(url, data):
    from app import logger
    try:
        data = json.dumps(data)
        data_rcv = post(url, data)
        if data_rcv:
            try:
                data_rcv = json.loads(data_rcv)
                return data_rcv
            except TypeError:
                logger.log('error trying to decode response (not a json).',level='ERROR')
                logger.log('data received: {}'.format(data_rcv), level='ERROR')
                return False
    except TypeError:
        logger.log('error trying to decode data provided (not json serializable).', level='ERROR')
        logger.log('data received: {}'.format(data), level='ERROR')
        return False
