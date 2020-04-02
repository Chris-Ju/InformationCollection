# -*- coding: utf-8 -*-
# Author: RTL
# Date: 2019.06.04

import pymysql

class db(object):
  
  def __init__(self, host, user, passwd, company):
    self.database = pymysql.connect(host, user, passwd, charset='utf8')
    self.cursor = self.database.cursor()
    self.cursor.execute('create database if not exists `%s`' % company)
    self.cursor.execute('use `%s`' % company)
    create_server_table = '''
    create table if not exists `server_table`(
      id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
      domain char(255),
      ip char(20),
      port char(255),
      source char(255),
      time timestamp DEFAULT CURRENT_TIMESTAMP
    ) AUTO_INCREMENT = 1 default charset = utf8
    '''
    create_status_table = '''
    create table if not exists `status_table`(
      id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
      ip char(20),
      domain char(255),
      port char(255),
      port_scan char(1) default '0',
      subdomain_enum char(1) default '0',
      ssl_search char(1) default '0',
      VirusTotal char(1) default '0',
      Dirsearch char(1) default '0',
      url_search_by_baidu char(1) default '0',
      url_search_by_360 char(1) default '0',
      time timestamp DEFAULT CURRENT_TIMESTAMP
    ) AUTO_INCREMENT = 1 default charset = utf8
    '''
    create_ip_history_table = '''
    create table if not exists `ip_history_table`(
      id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
      domain char(255),
      ip char(20),
      last_data char(255)
    ) AUTO_INCREMENT = 1 default charset = utf8
    '''
    create_ip_server_table = '''
      create table if not exists `ip_server_table`(
        id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        ip char(20),
        port char(5),
        server char(255),
        time timestamp DEFAULT CURRENT_TIMESTAMP
      ) AUTO_INCREMENT = 1 default charset = utf8;
    '''
    self.cursor.execute(create_server_table)
    self.cursor.execute(create_status_table)
    self.cursor.execute(create_ip_history_table)
    self.cursor.execute(create_ip_server_table)

  def __del__(self):
    self.database.close()

  def insert(self, table, col_name_value):
    query = 'insert into %s ( ' % table
    index = 0
    keys = list(col_name_value.keys())
    while index < len(keys) - 1:
      query += '%s, ' % keys[index]
      index += 1
    query += '%s ) values ( ' % keys[index]
    index = 0
    values = list(col_name_value.values())
    while index < len(values) - 1:
      query += '\'%s\', ' % values[index]
      index += 1
    query += '\'%s\' )' % values[index]
    try:
      self.cursor.execute(query)
      self.database.commit()
      return True
    except:
      self.database.rollback()
      return False

  def query(self, table, col_name, condition=None):
    query = 'select '
    index = 0
    while index < len(col_name) - 1:
      query += '%s, ' % col_name[index]
      index += 1
    query += '%s from %s' % (col_name[index], table)
    if condition is not None:
      query += ' where %s' % condition
    try:
      self.cursor.execute(query)
      return self.cursor.fetchall()
    except:
      return False

  def update(self, table, col_name_value, condition=None):
    query = 'update %s set ' % table
    index = 0
    items = list(col_name_value.items())
    while index < len(items) - 1:
      query += '%s=\'%s\', ' % items[index]
      index += 1
    query += '%s=\'%s\' ' % items[index]
    if condition is not None:
      query += 'where %s' % condition
    try:
      self.cursor.execute(query)
      self.database.commit()
      return True
    except:
      self.database.rollback()
      return False

  def delete(self, table, condition=None):
    query = 'delete from %s' % table
    if condition is None:
      return False
    query += 'where %s' % condition
    try:
      self.cursor.execute(query)
      self.database.commit()
      return True
    except:
      self.database.rollback()
      return False