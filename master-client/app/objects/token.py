#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import json, datetime

import requests.exceptions


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
                self.error = "invalid credentials"
                return False

        except requests.exceptions.InvalidURL:
            self.error = "invalid hostname"
            return False

        except requests.exceptions.ConnectionError:
            self.error = "connection error"
            return False