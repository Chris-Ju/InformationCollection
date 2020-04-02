# -*- coding: utf-8 -*-
# Author: RTL
# Date: 2019.06.04

import sys
import re
import requests
import threading
import time
import base64
import os
from . import DBOP

timeout = 2
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
  'Accept-Encoding': 'gzip, deflate'
}

# 获取 url
def so_get_url_count(site, method):
  try:
    url = 'https://www.so.com/s?ie=utf-8&q=%s%s' % (method, site)
    s = requests.get(url, headers=headers, timeout=2, verify=False, allow_redirects=False)  
    if s.text.find('<span class="nums" style="margin-left:20px">') > 0:
      number = re.findall(r'<span class="nums" style="margin-left:20px">找到相关结果约(.*?)个</span>', s.text, re.S)[0]
      count = int(number.replace(',', ''))
      return int(count / 10) + 1 
    else:
      return 0
  except:
    return 0

def so_get_url(website, method, pn=0, timeout=2):
  try:
    url = 'https://www.so.com/s?ie=utf-8&q=%s%s&pn=%d' % (method, website ,pn)
    s = requests.get(url, headers=headers, timeout=2, verify=False, allow_redirects=False)
    text = s.text
    urlqc = re.findall(r'<h3 class="res-title ">(.*?)</h3>', text, re.S)
    if urlqc:
      for i in urlqc:
        if i.find('data-url=') > 0:
          so_url_local = re.findall(r'data-url="(.*?)"', i, re.S)
        else:
          so_url_local = re.findall(r'<a href="(.*?)"', i, re.S)
        so_url_title = re.findall(r'target="_blank">(.*?)</a>', i, re.S)
        ss = requests.head(so_url_local[0], headers=headers, timeout=2, verify=False, allow_redirects=False)
        DBOP.insertNewUrl(so_url_local[0], ss.headers.get('Server'), so_url_title[0], "360")
  except:
    pass

def main(website, method):
  pn = so_get_url_count(website, method)
  for i in range(pn):
    so_get_url(website, method, i)
