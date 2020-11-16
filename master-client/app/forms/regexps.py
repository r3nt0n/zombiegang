#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import re
from flask import escape

class ValidRegex:
    IpAddress = re.compile(
        "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    )
    Hostname = re.compile(
        "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
    )
    Port = re.compile(
        "^(6553[0-5]|655[0-2][0-9]\d|65[0-4](\d){2}|6[0-4](\d){3}|[1-5](\d){4}|[1-9](\d){0,3})$"
    )
    HostPort = re.compile(
        "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9]):(6553[0-5]|655[0-2][0-9]\d|65[0-4](\d){2}|6[0-4](\d){3}|[1-5](\d){4}|[1-9](\d){0,3})$"
    )
    IpPort = re.compile(
        "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):(6553[0-5]|655[0-2][0-9]\d|65[0-4](\d){2}|6[0-4](\d){3}|[1-5](\d){4}|[1-9](\d){0,3})$"
    )
    EmailAddress = re.compile(
        "[^@]+@[^@]+\.[^@]+"
    )
    Username = re.compile(
        "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
    )
    Password = re.compile(
        "^(.*)$"
    )
    TaskType = re.compile(
        "^([a-zA-Z]{3})$"
    )


def validate(regex, input_str):
    if regex.match(input_str):
        return True
    return False


def sanitize(input_str):
    sanitized_data = escape(input_str)
    # ...
    return sanitized_data


# examples and testing
if __name__ == "__main__":
    print('ip address 192.168.1.400 matches: ')
    print(validate(ValidRegex.IpAddress, '192.168.1.400'))  # should be false

    print('ip address 192.168.1.1 matches: ')
    print(validate(ValidRegex.IpAddress, '192.168.1.1'))    # should be true

    print('port 5544455 matches: ')
    print(validate(ValidRegex.Port, '5544455'))    # should be false

    print('port 5555 matches: ')
    print(validate(ValidRegex.Port, '5555'))    # should be true

    print('hostport localhost:5555 matches: ')
    print(validate(ValidRegex.HostPort, 'localhost:5555'))  # should be true

    print('hostport 127.0.0.1:5555 matches: ')
    print(validate(ValidRegex.HostPort, '127.0.0.1:5555'))  # should be true

    print('hostname example.com matches: ')
    print(validate(ValidRegex.Hostname, 'example.com'))    # should be true

    print('hostname 5555 matches: ')
    print(validate(ValidRegex.Hostname, '5555'))    # should be true

    print('hostname 55$55.com matches: ')
    print(validate(ValidRegex.Hostname, '55$55.com'))  # should be false

    print('email 5555 matches: ')
    print(validate(ValidRegex.EmailAddress, '5555'))    # should be false

    print('email a@example.ocm matches: ')
    print(validate(ValidRegex.EmailAddress, 'a@example.ocm'))    # should be true