#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n custom logging module

import logging, os
from logging.handlers import RotatingFileHandler
from getpass import getpass


class color:
    PURPLE = u'\033[95m'
    CYAN = u'\033[96m'
    DARKCYAN = u'\033[36m'
    BLUE = u'\033[94m'
    GREEN = u'\033[92m'
    YELLOW = u'\033[93m'
    RED = u'\033[91m'
    BOLD = u'\033[1m'
    UNDERLINE = u'\033[4m'
    ORANGE = u'\033[33m'
    GREY = u'\033[90m'
    END = u'\033[0m'



class Logger:
    def __init__(self, debug=False, log_file=None, indent=0, input_pointer='>'):
        # initial settings
        self.debug = debug
        self.log_file = log_file
        self.indent = ''
        self.input_pointer = ' {} '.format(input_pointer)
        for i in range(0, indent):
            self.indent += ' '

        # colors by msg type
        self.color = {
            "DEBUG": color.PURPLE,
            "QUESTION": color.DARKCYAN,
            "INPUT": color.CYAN,
            "INFO": color.BLUE,
            "OPTION": color.CYAN,
            "SUCCESS": color.GREEN,
            "OTHER": color.YELLOW,
            "WARNING": color.ORANGE,
            "ERROR": color.RED,
            "CRITICAL": color.RED
        }

        # reference char by msg type
        self.ref_char = {
            "DEBUG": '-',
            "QUESTION": '?',
            "INPUT": 'i',
            "INFO": '+',
            "OPTION": '-',
            "SUCCESS": '+',
            "OTHER": '*',
            "WARNING": '!',
            "ERROR": '-',
            "CRITICAL": 'x'
        }

        # logs format with ISO-8601 format for timestamps
        self.console_format = logging.Formatter('%(message)s')
        #self.file_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        self.file_format = logging.Formatter('%(asctime)s | %(message)s')

        # default levels depending on debug == True/False
        self.default_console_level = logging.INFO
        self.default_file_level = logging.INFO

        # enable/disable debug mode
        if debug:
            self.default_console_level = logging.DEBUG
            self.default_file_level = logging.DEBUG

        # create logger and set default level to DEBUG (granular filters applied on individual handlers)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # init individual handlers
        self.console_handler = None
        self.logfile_handler = None

    def remove_console_handler(self):
        if self.console_handler:
            self.logger.handlers.remove(self.console_handler)
            self.console_handler = None

    def remove_logfile_handler(self):
        if self.logfile_handler:
            self.logger.handlers.remove(self.logfile_handler)
            self.logfile_handler = None

    def create_console_handler(self):
        # create console handler and set default level
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(self.default_console_level)
        if self.debug:
            self.console_handler.setFormatter(self.file_format)
        else:
            self.console_handler.setFormatter(self.console_format)
        self.logger.addHandler(self.console_handler)

    def create_logfile_handler(self):
        # create rotating file handler and set default level
        self.logfile_handler = RotatingFileHandler(self.log_file, maxBytes=2000, backupCount=10)
        self.logfile_handler.setLevel(self.default_file_level)
        self.logfile_handler.setFormatter(self.file_format)
        self.logger.addHandler(self.logfile_handler)

    def pretify(self, msg, level):
        if level == 'QUESTION':
            msg += self.input_pointer
        return '{}{}[{}]{} {}'.format(self.indent, self.color[level], self.ref_char[level], color.END, msg)

    def log(self, msg, level='INFO', pretty=True, overindent=0):
        if pretty:
            msg = self.pretify(msg, level)
        ind = ''
        for i in range(0, overindent):
            ind += ' '
        msg = ind+msg
        if level == 'DEBUG' or level == 'USER_INPUT' or level == 'QUESTION':
                self.logger.debug(msg)
        elif level == 'WARNING':
            self.logger.warning(msg)
        elif level == 'ERROR':
            self.logger.error(msg)
        elif level == 'CRITICAL':
            self.logger.critical(msg)
        else:
            self.logger.info(msg)

    def logged_input(self, question, hidden_value=False):
        if hidden_value:
            user_input = getpass(self.pretify(question, 'QUESTION'))
        else:
            user_input = input(self.pretify(question, 'QUESTION'))
        self.log(question, 'QUESTION')
        self.log(user_input, 'INPUT')
        return user_input

    def log_level(self, level):
        if level == 'DEBUG':
            return logging.DEBUG
        elif level == 'INFO':
            return logging.INFO
        elif level == 'WARNING':
            return logging.WARNING
        elif level == 'ERROR':
            return logging.ERROR
        elif level == 'CRITICAL':
            return logging.CRITICAL

    def set_level(self, handler, level):
        handler.setLevel(self.log_level(level))

    def start(self, console_log=True, file_log=False):
        if console_log:
            self.create_console_handler()
        if file_log and not self.log_file:
            self.log_file = os.path.basename(__file__)[:-3] + '.log'
        if self.log_file:
            self.create_logfile_handler()


