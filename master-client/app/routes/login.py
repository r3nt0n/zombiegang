#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask import Blueprint, current_app, render_template, redirect, url_for, request

from app import logger, zession
from app.forms import LoginForm


login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/', methods=['GET', 'POST'])
@login_bp.route('/index/', methods=['GET', 'POST'])
@login_bp.route('/login/', methods=['GET', 'POST'])
def login():
    zession.current_section = 'login'
    error = None
    if zession.token.jwt:
        return redirect(url_for("dashboard_bp.dashboard"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if request.method == 'POST':
            remote_host = request.form.get('remote_host')
            username = request.form.get('username')
            password = request.form.get('password')
            if zession.login(username, password, remote_host):
                return redirect(url_for("dashboard_bp.game"))
            else:
                error = zession.token.error
    return render_template("pages/login/login.html", login_form=login_form, error=error, zession=zession)


@login_bp.route('/not-authorized/', methods=['GET', 'POST'])
def not_authorized():
    return render_template("pages/errors/not-authorized.html")