#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


from flask import Blueprint, current_app, render_template, request

from datetime import datetime, timedelta

from app import logger, zession
from .custom_decorators import login_required
from app.modules.data_filter import DataFilter


logs_bp = Blueprint('logs_bp', __name__)


@logs_bp.route('/access-logs/', methods=['GET', 'POST'])
@login_required
def access_logs():
    zession.current_section = 'logs'
    data_type = 'access_logs'

    # first request get only last hour access logs
    filters = {'datetime_aft': (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')}
    data_filter = DataFilter(data_type, filters)
    # filter data
    data_filter.run(request)

    return render_template("pages/dashboard/logs/access-logs.html",
                           zession=zession, data_filter=data_filter)

