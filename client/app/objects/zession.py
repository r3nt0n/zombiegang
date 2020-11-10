#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import json, datetime

import requests

class Token:
    def __init__(self):
        self.jwt = ""
        self.error = None
        self.expiration_time = None

    def jwt_login(self, username, pswd, url="http://localhost:8080/api/login.php"):
        data = json.dumps( {"username": username, "pswd": pswd} )
        try:
            from app.modules.http_client import json_post
            data_rcv = json_post(url, data)
            if data_rcv and ("jwt" in data_rcv):
                #from app import logger; logger.log(data_rcv, 'ERROR')
                self.jwt = data_rcv["jwt"]
                self.expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                return self.jwt
            else:
                self.error = "Invalid credentials"
                return False

        except requests.exceptions.InvalidURL:
            self.error = "Hostname is required"
            return False

        except requests.exceptions.ConnectionError:
            self.error = "Invalid hostname"
            return False


class Zession:
    def __init__(self):
        self.remote_host = None
        self.username = None
        self.password = None
        self.current_section = None
        self.token = Token()

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

