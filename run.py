# -*- coding: utf-8 -*-
# Author: RTL
# Date: 2019.06.05

from Method import config, DBOP, ThreadManager
import IPS
import sys
import socket
import time

threading_pool = ThreadManager.ThreadPoolManger(3)

def main():
  domains = DBOP.GetAllDomain()
  for i in domains:
    config.domain_list.put((i[0], [1]))
  try:
    ip = socket.gethostbyname(config.domain)
  except:
    ip = 'Unknown'
  if int(DBOP.whetherInServer(config.domain)) == 0:
    DBOP.insertNewServer(config.domain, ip, source="Root")
  IPS.Rootmain(config.domain, ip)

  while True:
    if not config.domain_list.empty():
      domain, source = config.domain_list.get()
      try:
        ip = socket.gethostbyname(domain)
      except:
        ip = 'Unknown'
      if int(DBOP.whetherInServer(domain)) == 0:
        DBOP.insertNewServer(domain, ip, source=source)
      if config.domain not in domain:
        continue
      threading_pool.add_job(IPS.Nodemain, (domain, ip))
    elif threading_pool.work_queue.empty(): 
      break
    else:
      time.sleep(10)

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print('''
      python3 run.py example.com company
      Example:
      python3 run.py baidu.com baidu
    ''')
    exit(0)
  else:
    config.domain = sys.argv[1]
    config.company = sys.argv[2]
  main()