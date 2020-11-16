#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


from flask import Blueprint, current_app, send_from_directory, abort, safe_join

files_bp = Blueprint('files_bp', __name__)

import os

from app import logger
from .custom_decorators import login_required


@files_bp.route('/download-json/<filename>', methods=['GET'])
@login_required
def download_json(filename):
    dir = current_app.config['TEMP_DIR']
    try:
        return send_from_directory(dir, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
    finally:
        os.remove(safe_join(dir, filename))
        logger.log('tempfile {} deleted'.format(safe_join(dir, filename)), 'DEBUG')

