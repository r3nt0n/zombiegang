#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import requests, json

def update_user(zession, username, pswd):
    data = {'jwt': zession.jwt}
    if not (username and pswd):
        return False
    data['username'] = username
    data['pswd'] = pswd
    data = json.dumps(data)
    r = requests.post("http://{}/api/update_user.php".format(zession.remote_hostname), data=data)
    if r.status_code != 200:
        return False
    return json.loads(r.content.decode('utf-8-sig'))