#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import datetime

from app.components.token import Token


class RemoteZession:
    def __init__(self):
        self.remote_host = None
        self.username = None
        self.password = None
        self.current_section = None
        self.token = Token()

    def create_user(self, user, pswd, host):
        from app.modules import crud
        url = 'http://' + host + '/api/create_user.php'
        crud.create_data("user", data={"username": user, "pswd": pswd})


    def login(self, user, pswd, host):
        url = 'http://' + host + '/api/login.php'
        if self.token.jwt_login(user, pswd, url):
            self.remote_host = host
            self.username = user
            self.password = pswd
            return True
        return False

    def logout(self):
        self.remote_host = self.username = self.password = self.current_section = None
        self.token = Token()

    def check_for_refresh(self):
        if self.token.expiration_time <= datetime.datetime.now():
            self.token.jwt = self.token.jwt_login(self.username, self.password, 'http://' + self.remote_host + '/api/login.php')

