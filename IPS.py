# -*- coding: utf-8 -*-
# Author: RTL
# Date: 2019.06.05

from Method import baidu, so, config, DBOP, getDomainBySSL, nmapscan, subDomainsBrute, virusTotal

def SearchEngineerMain(domain, method):
  if DBOP.whetherDone('baidu', domain) != '2':
    DBOP.updateStatus('baidu', domain, '1')
    baidu.main(domain, method)
    DBOP.updateStatus('baidu', domain, '2')
  if DBOP.whetherDone('so', domain) != '2':
    DBOP.updateStatus('so', domain, '1')
    so.main(domain, method)
    DBOP.updateStatus('so', domain, '2')

def getDomainBySSLMain(domain):
  if DBOP.whetherDone('ssl', domain) != '2':
    DBOP.updateStatus('ssl', domain, '1')
    domains = getDomainBySSL.search_crt(domain)
    if domains is not False:
      for i in domains:
        config.domain_list.put((i, 'ssl'))
      DBOP.updateStatus('ssl', domain, '2')

def virusTotalMain(domain, root):
  if DBOP.whetherDone('VirusTotal', domain) != '2':
    DBOP.updateStatus('VirusTotal', domain, '1')
    if root and virusTotal.RootMain(domain) or not root and virusTotal.main(domain):
      DBOP.updateStatus('VirusTotal', domain, '2')

def subDomainsBruteMain(domain):
  if DBOP.whetherDone('subDomainBrute', domain) != '2':
    DBOP.updateStatus('subDomainBrute', domain, '1')
    result = subDomainsBrute.main(domain)
    if result is not False:
      for i in result:
        config.domain_list.put((i, "SubDomainBrute"))
      DBOP.updateStatus('subDomainBrute', domain, '2')
  
def nmapscanMain(ip):
  if ip == 'Unknown':
    return
  if DBOP.whetherDone('portScan', ip) != '2':
    DBOP.updateStatus('portScan', ip, '1')
    result = nmapscan.scan(ip)
    if result != {}:
      result = result[ip]
      for i in result.keys():
        DBOP.insertIpAndPort(ip, i, result[i]['product'])
    DBOP.updateStatus('portScan', ip, '2')
  else:
    DBOP.updateStatus('portScan', ip, '2')


def Rootmain(domain, ip):
  virusTotalMain(domain, True)
  getDomainBySSLMain(domain)
  SearchEngineerMain(domain, "site:")
  subDomainsBruteMain(domain)
  nmapscanMain(ip)

def Nodemain(domain, ip):
  virusTotalMain(domain, False)
  getDomainBySSLMain(domain)
  SearchEngineerMain(domain, "site:")
  nmapscanMain(ip)