#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

# the zombie http-client is build on top of urllib to remove dependencies (master http-client uses requests)

import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError


# urllib cheatsheet
def get(url):
    from app.components import logger
    logger.log('url: {}'.format(url), 'DEBUG')
    try:
        with urlopen(url) as response:
            response_content = response.read().decode('utf-8')
            return response_content
            # json_response = json.load(response)
            # response.getheader('Content-type') => 'application/json'
            # response.status => 200
            # response.reason => 'OK'
    except (HTTPError, URLError) as e:
        logger.log(url, 'CRITICAL')
        logger.log(e, 'CRITICAL')
        return False

# url = "http://localhost:8080"
# query_params = {"jwt": "DEMO_JWT", "date": "2019-04-11"}
def get_json(url, query_params=()):
    from app.components import logger
    logger.log('url: {}'.format(url), 'DEBUG')
    logger.log('params: {}'.format(query_params), 'DEBUG')
    try:
        query_string = urlencode(query_params)
        url = "?".join([url, query_string])
        with urlopen(url) as response:
            if response.status != 200:
                return False
            json_get_response = json.load(response)
        return json_get_response
    # except Exception as e:
    except (HTTPError, URLError) as e:
        logger.log(url, 'CRITICAL')
        logger.log(e, 'CRITICAL')
        return False


def post_json(url, data=()):
    from app.components import logger
    logger.log('url: {}'.format(url), 'DEBUG')
    logger.log('data_snd: {}'.format(data), 'DEBUG')
    try:
        custom_headers = {"Content-Type": "application/json"}
        json_post = Request(url, json.dumps(data, ensure_ascii=False).encode('utf-8'), custom_headers)
        with urlopen(json_post) as response:
            # if response.status != 200:
            #     return False
            json_post_response = json.load(response)
            logger.log('data_rcv: {}'.format(json_post_response), 'DEBUG')
        return json_post_response

    # except Exception as e:
    except (HTTPError, URLError) as e:
        logger.log(url, 'CRITICAL')
        logger.log(e, 'CRITICAL')
        return False


# url_file = "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.0.7.tar.xz"
# filename = 'latest-kernel.tar.xz'
def download_file(url_file, filename):
    from app.components import logger
    try:
        with urlopen(url_file) as response:
            with open(filename, 'wb') as f:
                while True:
                    # chunk references bytes read from response (16384 - 16 Kibibytes)
                    chunk = response.read(16384)
                    if chunk:
                        f.write(chunk)
                    else:
                        break
        logger.log('file {} successful downloaded'.format(url_file), 'SUCCESS')
        return True
    except Exception as e:
        # still need to catch some excepts
        # ...
        logger.log(url_file, 'ERROR')
        logger.log(e, 'ERROR')
        return False




