# -*- coding: utf-8 -*-
# Author: RTL
# Date: 2019.05.20

import requests
import time
from . import DBOP, config

apikey = ''

def RootMain(domain):
  url = 'https://www.virustotal.com/vtapi/v2/domain/report'
  params = {'apikey':apikey,'domain':domain}
  try:
    response = requests.get(url, params=params).json()
    try:
      ip_history = response['resolutions']
      for i in ip_history:
        DBOP.insertIpHistory(domain, i['ip_address'], i['last_resolved'])
    except:
      pass
    try:
      subdomain = response['subdomains']
      for i in subdomain:
        config.domain_list.put((i, 'VirusTotal'))
    except:
      pass
    return True
  except:
    return False

def main(domain):
  url = 'https://www.virustotal.com/vtapi/v2/domain/report'
  params = {'apikey':apikey,'domain':domain}
  try:
    response = requests.get(url, params=params)
    while response.status_code != 204:
      time.sleep(20)
      response = requests.get(url, params=params)
    response = response.json()
    ip_history = response['resolutions']
    for i in ip_history:
      DBOP.insertIpHistory(domain, i['ip_address'], i['last_resolved'])
    return True
  except:
    return False