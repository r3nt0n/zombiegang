#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

# the zombie http-client is build on top of urllib to remove dependencies (master http-client uses requests)

import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError


# urllib cheatsheet
#with urlopen("http://localhost:8080") as response:
    #response_content = response.read().decode('utf-8')
    #json_response = json.load(response)
    # response.getheader('Content-type') => 'application/json'
    # response.status => 200
    # response.reason => 'OK'

# url = "http://localhost:8080"
# query_params = {"jwt": "DEMO_JWT", "date": "2019-04-11"}
# GET
def get_json(url, query_params=()):
    query_string = urlencode(query_params)
    url = "?".join([url, query_string])
    with urlopen(url) as response:
        if response.status != 200:
            return False
        json_get_response = json.load(response)
    return json_get_response

# # POST example
# post_data = urlencode(query_params).encode('ascii')
# with urlopen(url, post_data) as response:
#     post_response = json.load(response)


# url_file = "https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.0.7.tar.xz"
# filename = 'latest-kernel.tar.xz'
def download_file(url_file, filename):
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
        return True
    except:
        return False

# POST json data in the request
def post_json(url, data=()):
    from app.components import logger
    custom_headers = {"Content-Type": "application/json"}
    try:
        logger.log('url: {}'.format(url), 'DEBUG')
        logger.log('data_snd: {}'.format(data), 'DEBUG')
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


