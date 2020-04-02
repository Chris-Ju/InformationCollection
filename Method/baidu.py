# -*- coding: utf-8 -*-
# Author: RTL
# Date: 2019.06.04

import re
import requests
from urllib.parse import urlparse
import time
from . import DBOP

timeout = 2  # 超时时间
headers = {  # HTTP 头设置
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
  'Accept-Encoding': 'gzip, deflate'
}

def baidu_get_url(website, method, pn=0, timeout=2):
  url = 'http://www.baidu.com/s?wd=%s%s&pn=%d' % (method, website, pn)
  try:
    s = requests.get(url, headers=headers, timeout=timeout, allow_redirects=False)
    text = s.text
    urlqc = re.findall(r'data-tools=\'\{"title":(.*?)}\'>', text, re.S)
    if urlqc:
      for i in urlqc:
        url_baidu_title = re.findall(r'"(.*?)","', i, re.S)
        url_local = re.findall(r'"url":"(.*?)"', i, re.S)
        if url_local:
          ss = requests.get(url_local[0], headers=headers, timeout=timeout, allow_redirects=False)
          DBOP.insertNewUrl(ss.headers['Location'], ss.headers.get('Server'), url_baidu_title[0], "baidu")
  except:
    pass


def baidu_get_url_count(website, method):
  try:
    url = 'http://www.baidu.com/s?wd=%s%s' % (method, website)
    s = requests.get(url, headers=headers, timeout=2, allow_redirects=False)
    text = s.text
    number = re.findall(r'<span class="nums_text">百度为您找到相关结果约(.*?)个</span>', text, re.S)[0]
    count = int(number.replace(',', ''))
    if count > 500:
      return 500
    else:
      return count
  except:
    return 0

def main(website, method):
  baidu_pn = baidu_get_url_count(website, method)
  baidu_pm = int(baidu_pn / 10) + 1
  for i in range(baidu_pm):
    pg = i * 10
    baidu_get_url(website, method, pg)