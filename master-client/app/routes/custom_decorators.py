#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask import redirect, url_for

from functools import wraps

from app import zession


# login requirements
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #logger.log(zession, 'DEBUG')
        if zession.token.jwt == '':
            return redirect(url_for('login_bp.not_authorized'))
        else:
            zession.check_for_refresh()
        return f(*args, **kwargs)
    return decorated_function