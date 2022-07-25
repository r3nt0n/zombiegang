#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

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
    from app.components import logger
    value = ''
    low_permises = False
    if platform.system() == 'Windows':
        value = get_win_reg(name, winreg.HKEY_LOCAL_MACHINE, r"Software\MSExcel")
        if not value:
            low_permises = True

    if platform.system() == 'Linux' or low_permises:
        if os.path.exists(path):
            logger.log('loading {} from file'.format(name), 'INFO')
            with open(path, 'r') as f:
                value = f.read()
        else:
            return False

    if value:
        try:
            value = json.loads(value)
            logger.log(value, 'DEBUG')
            return value
        except:
            return False
    return False


def set_zombie_settings(path, name, value):
    from app.components import logger
    value = json.dumps(value, ensure_ascii=False)

    low_permises = False
    if platform.system() == 'Windows':
        if not set_win_reg(name, value, winreg.HKEY_LOCAL_MACHINE, r"Software\MSExcel"):
            low_permises = True
    if platform.system() == 'Linux' or low_permises:
        if not os.path.exists(path):
            try:
                os.makedirs(os.path.dirname(path))
            except FileExistsError:
                pass
        with open(path, 'w') as f:
            logger.log('writing {} to file {}'.format(name, path), 'INFO')
            f.write(value)
        return True

