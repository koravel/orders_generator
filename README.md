# Requirements
* Python and packages:
  - python 3.7+
  - pika 1.0.0+
  - mysql-connector 2.1.6+
* mysql server 8.0+
* rabbitmq 3.7.13

# Usage details
1. DBand table name:
```
create database test;
use test;
create table order_notes(
order_id decimal(20,0) unsigned NOT NULL,
status char(16) NOT NULL,
timestamp decimal(13,3) unsigned NOT NULL,
currency_pair char(16) NOT NULL,
order_direction char(4) NOT NULL,
init_price float(6,5) NOT NULL,
fill_price float(6,5) NOT NULL,
init_volume float(13,8) NOT NULL,
fill_volume float(13,8) NOT NULL,
description text default null,
tags tinytext default null
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
2. If app moved to another PC and pathes to settings, log folder etc. is not remote, delete pathes.json to re-initialize it

3. Do not delete root.py - file indicates root of app to all components

4. If settings.json empty or not presented, settings-default.json is used insead

5. If settings.json empty or not presented, settings-default.json is used insead

Feel free to modify app)
