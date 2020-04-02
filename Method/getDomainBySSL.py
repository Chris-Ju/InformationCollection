# -*- coding: utf-8
# Author: RTL
# Date: 2019.06.04

import requests
import json

def search_crt(domain):
    subdomain_list = []
    request_url = 'https://crt.sh/?q=%.{}&output=json'.format(domain)
    try:
      request_json = requests.get(request_url, timeout=10)
    except:
      return False

    if request_json.status_code != 200:
        return False
    request_json = request_json.text.replace('}{', '},{')
    fixed_json = json.loads('[{}]'.format(request_json))
    for extension_id, value in enumerate(fixed_json[0]):
        subdomain = value['name_value']
        subdomain_list.append(subdomain)
    return list(set(subdomain_list))

