-- drop table if exists order_records;
create table order_records(
id decimal(20) unsigned NOT NULL,
order_id decimal(20) unsigned NOT NULL,
status char(16) NOT NULL,
currency_pair char(16) NOT NULL,
direction char(16) NOT NULL,
init_price float(6,5) NOT NULL,
fill_price float(6,5) NOT NULL,
init_volume float(13,8) NOT NULL,
fill_volume float(13,8) NOT NULL,
tags tinytext default null,
description text default null,
timestamp decimal(20) unsigned NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;