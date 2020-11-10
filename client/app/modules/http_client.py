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
    #logger.log('r.content: {}'.format(r.content), level='DEBUG')
    #logger.log('r.text: {}'.format(r.text), level='DEBUG')
    if r.status_code != 200:
        data_rcv = ''
        logger.log('{} http code received'.format(r.status_code), level='ERROR')
    else:
        data_rcv = r.content.decode('utf-8-sig')

        logger.log('{} http code received'.format(r.status_code), level='SUCCESS')
    #logger.log('response: {}'.format(r.content.decode('utf-8-sig')), level='DEBUG')
    return data_rcv


def json_post(url, data):
    from app import logger
    data_rcv = post(url, data)
    if data_rcv:
        try:
            data_rcv = json.loads(data_rcv)
            return data_rcv
        except TypeError:
            logger.log('error trying to decode response (not a json).',level='ERROR')
            logger.log('data received: {}'.format(data_rcv), level='ERROR')
            return False
    return False
