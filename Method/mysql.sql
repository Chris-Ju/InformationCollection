create table server_table(
  id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  uid char(32),
  domain char(255),
  ip char(20),
  port char(255),
  source char(255),
  time timestamp DEFAULT CURRENT_TIMESTAMP
) AUTO_INCREMENT = 1 default charset = utf8;


create table status_table(
  id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  ip char(20),
  domain char(255),
  port char(5),
  port_scan char(1) default '0',
  subdomain_enum char(1) default '0',
  ssl_search char(1) default '0',
  VirusTotal char(1) default '0',
  Dirsearch char(1) default '0',
  url_search_by_baidu char(1) default '0',
  url_search_by_360 char(1) default '0',
  time timestamp DEFAULT CURRENT_TIMESTAMP
) AUTO_INCREMENT = 1 default charset = utf8;

create table ip_server_table(
  id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  ip char(20),
  port char(5),
  server char(255),
  time timestamp DEFAULT CURRENT_TIMESTAMP
) AUTO_INCREMENT = 1 default charset = utf8;

create table ip_history_table(
  id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  domain char(255),
  ip char(20),
  last_data char(255)
) AUTO_INCREMENT = 1 default charset = utf8;

