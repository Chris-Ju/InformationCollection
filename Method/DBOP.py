# -*- coding: utf-8 -*-
# Author: Chris Ju
# Date: 2019.04.08

import re
import sys
import hashlib
from urllib.parse import urlparse
from . import config, mongodb, mysqldb


# 方法名与数据库列名对应
dic = {
  "baidu" : "url_search_by_baidu",
  "so": "url_search_by_360",
  "subDomainBrute": "subdomain_enum",
  "portScan": "port_scan",
  "ssl": "ssl_search",
  "VirusTotal": "VirusTotal",
  "Dirsearch": "Dirsearch"
}

mysqldb = mysqldb.db(config.host, config.user, config.password, sys.argv[2].replace('.', '_'))
mongodb = mongodb.db(config.host, config.mongodb_port, sys.argv[2].replace('.', '_'))


# 判断方法是否完成
def whetherDone(method, domain):
  while config.lock:
    continue
  config.lock = True
  try:
    if method != "portScan":
      result = mysqldb.query("status_table", [dic[method]], "domain='%s'" % domain)[0][0]
    else:
      result = mysqldb.query("status_table", [dic[method]], "ip='%s'" % domain)
      for i in result:
        if i[0] == '2':
          result = '2'
          break
  except:
    result = '2'
  config.lock = False
  return result

# 更新方法状态
def updateStatus(method, domain, status):
  while config.lock:
    continue
  config.lock = True
  if method != "portScan":
    result = mysqldb.update("status_table", {dic[method]: status}, "domain='%s'" % domain)
  else:
    result = mysqldb.update("status_table", {dic[method]: status}, "ip='%s'" % domain)
  config.lock = False
  return result

# 判断域名是否存在
def whetherInServer(domain):
  while config.lock:
    continue
  config.lock = True
  result = mysqldb.query("server_table", ["count(*)"], "domain='%s'" % domain)[0][0]
  config.lock = False
  return result

# 判断 ip 端口是否存在
def IpPortwhetherInServer(ipAndPort):
  ip, port, server = ipAndPort
  while config.lock:
    continue
  config.lock = True
  result = mysqldb.query("ip_server_table", ["count(*)"], "ip='%s' and port='%s'" % (ip, str(port)))[0][0]
  config.lock = False
  return result

# 通过 ip 获取域名
def GetDomainByIp(ip, domain):
  while config.lock:
    continue
  config.lock = True
  result = mysqldb.query("server_table", ['domain'], "ip='%s' and domain REGEXP '%s'" % (ip, domain))
  config.lock = False
  return result

# 获取所有服务
def GetAllDomain():
  while config.lock:
    continue
  config.lock = True
  result = mysqldb.query("server_table", ['domain', 'source'], "domain!=''")
  config.lock = False
  return result

# 获取来源
def GetSource(domain):
  while config.lock:
    continue
  config.lock = True
  try:
    result = mysqldb.query("server_table", ['source'], "domain='%s'" % domain)[0][0]
  except:
    result = ""
  config.lock = False
  return result

# 获取关于域名的所有 ip
def getIP(domain):
  while config.lock:
    continue
  config.lock = True
  try:
    result = mysqldb.query("server_table", ['ip'], "domain regexp '%s'" % domain)
  except:
    result = []
  config.lock = False
  return result

# 插入 Ip port
def insertIpAndPort(ip, port, server):
  value = {
    'ip': ip,
    'port': port,
    'server': server
  }
  while config.lock:
    continue
  config.lock = True
  result = mysqldb.insert("ip_server_table", value)
  config.lock = False
  return result

# 插入 Ip History
def insertIpHistory(domain, ip, date):
  value = {
    'domain': domain,
    'ip': ip,
    'last_data': date
  }
  while config.lock:
    continue
  config.lock = True
  result = mysqldb.insert("ip_history_table", value)
  config.lock = False
  return result

# 插入新的服务
def insertNewServer(domain, ip, port='', source=''):
  value_1 = {
    'domain': domain,
    'ip': ip,
    'port': port,
    'source': source
  }
  value_2 = {
    'ip': ip,
    'domain': domain,
    'port': port
  }
  while config.lock:
    continue
  config.lock = True
  result = mysqldb.insert("server_table", value_1) and mysqldb.insert("status_table", value_2)
  config.lock = False
  return result

# 插入新的 url
def insertNewUrl(url, server, title, method):
  if re.match('http[s]*://', url) is None:
    url = "http://" + url    
  scheme, netloc, path, params, query, fragment = urlparse(url)[0:6]
  netloc = netloc.split(':')
  if len(netloc) == 2:
    domain, port = netloc
  else:
    domain = netloc[0]
    if scheme == 'https':
      port = 443
    else:
      port = 80
  if config.domain in domain:
    config.domain_list.put((domain, method))
  val = {
    'domain' : domain,
    'port' : port,
    'path' : path,
    'url' : url,
    'param' : query,
    'flagment' : fragment,
    'title' : title,
    'Method': method,
    'Server': server
  }
  return mongodb.insert("URL", val)
