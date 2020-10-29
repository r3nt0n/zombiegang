#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import requests, json, datetime

class Token:
    def __init__(self):
        self.jwt = ""
        self.jwt_json = { 'jwt': self.jwt }
        self.error = None
        self.expiration_time = None

    def jwt_login(self, username, pswd, hostname="localhost:8080"):
        data = json.dumps( {"username": username, "pswd": pswd} )
        try:
            login = requests.post("http://{}/api/login.php".format(hostname), data=data)
            data_rcv = json.loads(login.content)

            if "jwt" in data_rcv:
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

    def check_for_refresh(self, zession):
        if self.expiration_time <= datetime.datetime.now():
            zession.jwt = self.jwt_login(zession.username, zession.pswd, zession.hostname)





