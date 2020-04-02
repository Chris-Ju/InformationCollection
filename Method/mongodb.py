# -*- coding: utf-8 -*-
# Author: RTL
# Date: 2019.06.04

import pymongo

class db(object):

  def __init__(self, host, port, database):
    self.client = pymongo.MongoClient(host, port)
    self.database = self.client[database]

  def insert(self, collection, val):
    try:
      self.database[collection].insert(val)
      return True
    except:
      return False
  
  def query(self, collection, condition={}):
    try:
      results = self.database[collection].find(condition)
      temp = []
      for i in results:
        temp.append(i)
      return temp
    except:
      return False

  def update(self, collection, val, condition={}):
    try:
      result = self.database[collection].update(condition, {'$set': val})
      return result.nModified
    except:
      return False

  def remove(self, collection, condition={}):
    try:
      result = self.database[collection].remove(condition)
      return result.n
    except:
      return False