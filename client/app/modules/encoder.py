#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import json

def pack_task(task_content):
    try:
        json_task = json.dumps(task_content)
        encoded_json_task = json_task.encode()
        return encoded_json_task
    except:
        return False

def unpack_task(encoded_json_task):
    try:
        decoded_json_task = encoded_json_task.decode()
        task_content = json.load(decoded_json_task)
        return task_content
    except:
        return False


