#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


from flask import Blueprint, render_template, request

from app import zession

from app.forms import EditProfileForm

from app.controllers import DataFilter
from app.modules.crud import create_data, read_data, update_data, delete_data

from .custom_decorators import login_required

members_bp = Blueprint('members_bp', __name__)


@members_bp.route('/zombies/', methods=['GET', 'POST'])
@members_bp.route('/zombies/<zid>/', methods=['GET', 'POST'])
@login_required
def zombies(zid=None):
    zession.current_section = 'members'
    data_type = 'zombies'

    zombies_created = []
    zombies_deleted = []
    users_deleted = []
    detailed_zombie = False

    # prepare filters
    data_filter = DataFilter(data_type)
    # filter data
    data_filter.run(request)

    if zid is not None:
        for row in data_filter.data:
            if row["id"] == zid:
                detailed_zombie = row

    # get join requests
    zombie_requests = read_data('users', {"not_in": "zombies,masters"})

    # create zombies
    if (request.method == 'POST') and (('btn-create-zombies' in request.form) and zombie_requests):
        selected_users = request.form.getlist('users_checked')
        # logger.log('request.form: '.format(request.form), 'DEBUG')
        # logger.log('selected_users: '.format(selected_users), 'DEBUG')
        for user in zombie_requests:
            if user['username'] in selected_users:
                # create zombie
                zombie_data = {
                    'username': user['username'],
                    'current_public_ip': user['public_ip'],
                    'current_country': user['country']
                }
                if create_data('zombie', zombie_data):
                    zombies_created.append(user['username'])

    # delete zombies
    elif (request.method == 'POST') and ('btn-delete-zombies' in request.form):
        selected_zombies = request.form.getlist('zombies_checked')
        for username in selected_zombies:
            if delete_data('zombie', username):
                zombies_deleted.append(username)

    # delete users
    elif (request.method == 'POST') and ('btn-delete-users' in request.form):
        selected_users = request.form.getlist('users_checked')
        for username in selected_users:
            if delete_data('user', username):
                users_deleted.append(username)


    return render_template("pages/dashboard/members/zombies.html", zession=zession, data_filter=data_filter,
                           zombie_requests=zombie_requests, zombies_created=zombies_created,
                           zombies_deleted=zombies_deleted, users_deleted=users_deleted, detailed_zombie=detailed_zombie)


@members_bp.route('/masters/', methods=['GET', 'POST'])
@login_required
def masters():

    zession.current_section = 'members'
    data_type = 'masters'

    update_error = None
    edit_profile = False
    edit_profile_form = EditProfileForm()

    # launch edit profile window
    if (request.method) == 'POST' and ('btn-launcher' in request.form):
        edit_profile = True

    # update profile
    elif (request.method) == 'POST' and not ('btn-launcher' in request.form or 'filter_btn' in request.form):
        # update master password
        if ('pswd_btn' in request.form):
            if not request.form.get('password'):
                update_error = 'introduce the new password'
            else:
                response = update_data('user', {'username': zession.username, 'pswd': request.form.get('password')})
                update_error = 'could not contact server'
                if response and ('jwt' in response):
                    zession.jwt = response['jwt']
                    update_error = 'password updated'

        # update master public key
        elif ('public_key_btn' in request.form):
            if edit_profile_form.validate_on_submit():
                if not request.form.get('public_key'):
                    update_error = 'introduce the new public_key'
                # ...

    # filter data
    data_filter = DataFilter(data_type)
    # filter data
    data_filter.run(request)

    return render_template("pages/dashboard/members/masters.html",
                           zession=zession, data_filter=data_filter,
                           update_error=update_error, edit_profile=edit_profile, edit_profile_form=edit_profile_form)

