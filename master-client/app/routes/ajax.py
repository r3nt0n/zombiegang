#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import json
from datetime import datetime

from flask import Blueprint, current_app, request, render_template, jsonify, escape, url_for

from app import logger, proxy
from app.forms.regexps import validate, ValidRegex

ajax_bp = Blueprint('ajax_bp', __name__)


@ajax_bp.route('/ajax/get-actual-ip', methods=['POST'])
def get_actual_ip():
    proxy.get_actual_ip()
    flag = render_template('objects/dynamic/cc_flag.html', country_code=proxy.country)
    return jsonify({'ip': proxy.current_ip, 'country': proxy.country, 'flag': flag})


@ajax_bp.route('/ajax/toggle-proxy', methods=['POST'])
def toggle_proxy():
    enabled = 'false'
    if proxy.host:
        proxy.remove()
        logger.log('socks5 proxy session {}:{} removed'.format(proxy.host, proxy.port), 'INFO')
    else:
        input_host = request.form.get('host')
        input_port = request.form.get('port')
        if (validate(ValidRegex.IpAddress, input_host) or validate(ValidRegex.Hostname, input_host)) and validate(ValidRegex.Port, input_port):
            input_host = str(escape(input_host))
            input_port = int(escape(input_port))
            proxy.get_socks5_session(input_host, input_port)
            enabled = 'true'
            logger.log('socks5 proxy session {}:{} created'.format(proxy.host, proxy.port), 'SUCCESS')
        else:
            logger.log('regexp error in {}:{} while trying to create socks5 proxy session'.format(proxy.host, proxy.port), 'ERROR')

    return jsonify({'enabled': enabled})


@ajax_bp.route('/ajax/is-proxy-enabled', methods=['POST'])
def is_proxy_enabled():
    host = port = ''
    enabled = 'false'
    if proxy.host:
        enabled = 'true'
        host = proxy.host
        port = str(proxy.port)
    return jsonify({'enabled': enabled, 'host': host, 'port': port})


@ajax_bp.route('/ajax/json-export', methods=['POST'])
def json_export():
    data_type = request.form.get('data_type')
    data = json.loads(request.form.get('data'))
    selected_data_ids = request.form.get('data_checked')

    column_id = 'id'
    if (data_type == 'users') or (data_type == 'zombies') or (data_type == 'masters'):
        column_id = 'username'

    selected_data = [row for row in data if row[column_id] in selected_data_ids]

    filename = (datetime.now()).strftime('%Y%m%d_%H%M%S') + '-' + data_type + '.json'
    with open(current_app.config['TEMP_DIR'] + filename, 'w') as temp:
        json.dump(selected_data, temp, indent=4)
    logger.log('tempfile {} created'.format(current_app.config['TEMP_DIR'] + filename), 'DEBUG')
    # here returns the url to get the file to ajax call
    return jsonify({'url': url_for('files_bp.download_json', filename=filename)})

