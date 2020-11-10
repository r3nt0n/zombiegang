#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask import Blueprint, render_template, redirect, url_for, request, escape

from app import config, logger, zession


login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/', methods=['GET', 'POST'])
@login_bp.route('/index/', methods=['GET', 'POST'])
@login_bp.route('/login/', methods=['GET', 'POST'])
def login():
    zession.current_section = 'login'
    error = None
    # print(zession)
    if zession.token.jwt:
        return redirect(url_for("login_bp.dashboard"))
    if request.method == 'POST':
        hostname = escape(request.form.get('hostname'))
        username = escape(request.form.get('username'))
        pswd = escape(request.form.get('pswd'))
        if zession.login(username, pswd, hostname):
            return redirect(url_for("dashboard_bp.game"))
        else:
            error = zession.token.error
    return render_template("pages/login/login.html", error=error, zession=zession)


@login_bp.route('/not-authorized/', methods=['GET', 'POST'])
def not_authorized():
    return render_template("pages/errors/not-authorized.html")