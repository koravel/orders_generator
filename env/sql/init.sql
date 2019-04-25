create database if not exists `gen_db`;

use `gen_db`;

drop table if exists `order_records`;
drop table if exists `direction`;
drop table if exists `status`;

create table `direction`(
id int unsigned NOT NULL auto_increment,
title char(16) NOT NULL,
primary key(id)
)DEFAULT CHARSET=utf8;

create table `status`(
id int unsigned NOT NULL auto_increment,
title char(16) NOT NULL,
primary key(id)
)DEFAULT CHARSET=utf8;

create table `order_records`(
order_id decimal(20) unsigned NOT NULL,
`timestamp` decimal(20,0) unsigned NOT NULL,
`status` int unsigned NOT NULL,
currency_pair char(16) NOT NULL,
direction INT unsigned NOT NULL,
init_price float(6,5) NOT NULL,
fill_price float(6,5) NOT NULL,
init_volume float(13,8) NOT NULL,
fill_volume float(13,8) NOT NULL,
tags tinytext default null,
description text default null,
PRIMARY KEY (order_id, `status`),
FOREIGN KEY (`status`)  REFERENCES `status` (id),
FOREIGN KEY (direction)  REFERENCES `direction` (id)
)DEFAULT CHARSET=utf8;

insert into direction(title) values('Buy'),('Sell');
insert into `status`(title) values('New'),('To provider'),('Rejected'),('Partial filled'),('Filled');