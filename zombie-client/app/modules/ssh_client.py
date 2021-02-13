#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

# the zombie http-client is build on top of urllib to remove dependencies (master http-client uses requests)

import json
import paramiko
import socket
import time


def ssh_login(hostname, username, password, delay=60):
    from app.components import logger

    # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)

    except socket.timeout:
        # this is when host is unreachable
        logger.log('Host {} is unreachable'.format(hostname), 'ERROR')
        return False

    except paramiko.AuthenticationException:
        logger.log("Invalid credentials for {}:{} in {}".format(username, password, hostname), 'DEBUG')
        return False

    except paramiko.SSHException:
        logger.log("Quota exceeded, sleeping for {} seconds...".format(delay), 'WARNING')
        # sleep for a minute
        time.sleep(delay)
        return ssh_login(hostname, username, password)

    else:
        # connection was established successfully
        logger.log("Connection was established succesfully", 'SUCCESS')
        return True

