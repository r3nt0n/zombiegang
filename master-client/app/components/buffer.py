#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


class Buffer:
    def __init__(self):
        self.data = {}

    def store(self, data_type, data):
        self.data[data_type] = data

    def clear(self, data_type='all'):
        if data_type == 'all':
            self.data = {}
        else:
            self.data[data_type] = None
