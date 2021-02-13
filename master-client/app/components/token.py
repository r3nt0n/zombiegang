#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import datetime

import requests.exceptions


class Token:
    def __init__(self):
        self.jwt = ""
        self.error = None
        self.expiration_time = None

    def jwt_login(self, username, pswd, url):
        try:
            from app.modules.crud import login
            data_rcv = login(username, pswd, url)
            if data_rcv:
                self.jwt = data_rcv
                self.expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
                return self.jwt

            self.error = "invalid credentials"
            return False

        except requests.exceptions.InvalidURL:
            self.error = "invalid hostname"
            return False

        except requests.exceptions.ConnectionError:
            self.error = "connection error"
            return False