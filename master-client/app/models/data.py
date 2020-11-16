#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import json
from base64 import b64encode, b64decode

from app import logger
from app.modules import crud

class Data:
    def __init__(self):
        self.name = 'data'
        self.id = ''
        self.created_at = ''
        self.updated_at = ''

    def pack_value(self, value):
        try:
            json_value = json.dumps(value)
            encoded_json_value = json_value.encode()
            b64_value = b64encode(encoded_json_value)
            return b64_value
        except:
            return False

    def unpack_value(self, b64_value):
        try:
            encoded_json_value = b64decode(b64_value)
            json_value = encoded_json_value.decode()
            value = json.load(json_value)
            return value
        except:
            return False

    def merge_values(self, value_a, value_b):
        if value_a is None:
            value_a = ''
        if value_b is None:
            value_b = ''
        return ((value_a + ' ' + value_b).rstrip()).lstrip()

    def create(self, data):
        # ... subclasses create methods runs here
        post_data = {}
        for attr, value in self.__dict__.items():
            if value:  # dont post empty values
                post_data[attr] = value
        logger.log('post_data: {}'.format(post_data), 'WARNING')
        response = crud.create_data(self.name, post_data)
        logger.log('response: {}'.format(response), 'WARNING')
        if response and 'id' in response:
            self.id = response['id']
            return True
        return False

    def update(self, data):
        # ... subclasses create methods runs here
        data = {}
        for attr, value in self.__dict__.items():
            data[attr] = value
        if crud.update_data(self.name, data):
            return True
        return False