# -*- coding: utf-8 -*-
# Author: RTL
# Date: 2019.06.04

from ESD import EnumSubDomain

def main(domain):
  try:
    domains = EnumSubDomain(domain).run()
    return domains
  except:
    return False