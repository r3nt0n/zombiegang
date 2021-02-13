#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask import Blueprint, render_template, redirect, url_for, request

from app import zession
from app.forms import LoginForm


login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/', methods=['GET', 'POST'])
@login_bp.route('/index/', methods=['GET', 'POST'])
def index():
    zession.current_section = 'login'
    if zession.token.jwt:
        return redirect(url_for("dashboard_bp.dashboard"))

    return render_template("pages/login/index.html", zession=zession, state='logout')



@login_bp.route('/login/', methods=['GET', 'POST'])
def login():
    zession.current_section = 'login'
    error = None
    if zession.token.jwt:
        return redirect(url_for("dashboard_bp.dashboard"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if request.method == 'POST':
            zession.remote_host = request.form.get('remote_host')
            username = request.form.get('username')
            password = request.form.get('password')
            # create user
            if 'create_btn' in request.form:
                zession.create_user(username, password, zession.remote_host)
            # login
            if zession.login(username, password, zession.remote_host):
                return redirect(url_for("dashboard_bp.game"))
            else:
                zession.remote_host = None
                error = zession.token.error

    return render_template("pages/login/login.html", login_form=login_form, error=error, zession=zession)


@login_bp.route('/not-authorized/', methods=['GET', 'POST'])
def not_authorized():
    return render_template("pages/errors/not-authorized.html")