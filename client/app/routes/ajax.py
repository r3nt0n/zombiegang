#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask import Blueprint, request, render_template, jsonify

from app import logger, proxy


ajax_bp = Blueprint('ajax_bp', __name__)


@ajax_bp.route('/ajax/get-actual-ip', methods=['POST'])
#@login_required
def get_actual_ip():
    #return jsonify({'text': proxy.get_actual_ip(request.form['text'])})
    proxy.get_actual_ip()
    flag = render_template('objects/dynamic/cc_flag.html', country_code=proxy.country)
    return jsonify({'ip': proxy.current_ip, 'country': proxy.country, 'flag': flag})


@ajax_bp.route('/ajax/toggle-proxy', methods=['POST'])
def toggle_proxy():
    # logger.log('ajax data received: ', 'DEBUG')
    # logger.log('request.form.host: '.format(request.form.get('host')), 'DEBUG')
    # logger.log('request.form.port: '.format(request.form.get('port')), 'DEBUG')
    if proxy.host:
        proxy.remove()
        enabled = 'false'
        logger.log('socks5 proxy session {}:{} removed'.format(proxy.host, proxy.port), 'INFO')
    else:
        proxy.get_socks5_session(request.form.get('host'), int(request.form.get('port')))
        enabled = 'true'
        logger.log('socks5 proxy session {}:{} created'.format(proxy.host, proxy.port), 'INFO')
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

