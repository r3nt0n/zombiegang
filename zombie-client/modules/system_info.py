#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import socket, platform

from modules import httpz

def get_private_ip():
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        temp_socket.connect(('10.255.255.255', 0))
        ip = temp_socket.getsockname()[0]
    except: ip = '127.0.0.1'
    finally: temp_socket.close()
    return ip


def get_public_ip_cc():
    try:
        data = httpz.post_json('https://api.myip.com/')
        return (data['ip'], data['cc'])
    except:
        return False


def get_hostname():
    # return os.uname()[1]
    # test which works on windows
    #return socket.gethostname()
    return platform.node()



def get_mac_addr():
    pass
    # return current_mac_addr

