#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


from flask import Blueprint, current_app, render_template, redirect, url_for

dashboard_bp = Blueprint('dashboard_bp', __name__)

from app import logger, zession
from .custom_decorators import login_required


@dashboard_bp.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    zession.logout()
    return redirect(url_for("login_bp.login"))


@dashboard_bp.route('/game/', methods=['GET', 'POST'])
@login_required
def game():
    return render_template("pages/login/game.html", zession=zession)


@dashboard_bp.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("pages/dashboard/base_dashboard.html", zession=zession)
