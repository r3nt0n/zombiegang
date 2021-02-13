#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

# just initial scratches and notes

import scapy

class SYNFlood:
    def __init__(self, ip="192.168.1.1", port=80):
        self.ip = ip
        self.port = port
        # forge IP packet with target ip as the destination IP address
        ip = scapy.IP(dst=self.ip)
        # or if you want to perform IP Spoofing (will work as well)
        # ip = IP(src=RandIP("192.168.1.1/24"), dst=target_ip)