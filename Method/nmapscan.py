# -*- coding: utf-8 -*-
# Author: RTL
# Date: 2019.06.04

import nmap

def scan(ip):
  nm = nmap.PortScanner()
  nm.scan(ip)
  result = {}
  for host in nm.all_hosts():
    temp = {}
    for proto in nm[host].all_protocols():
      for port in nm[host][proto].keys():
        temp[port] = nm[host][proto][port]
    result[host] = temp
  return result