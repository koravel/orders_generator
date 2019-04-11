# What is it?
This is simply app created for generate data objects named 'Order Record' and 'Order'.
Primary object is 'Order'. 'Order' can have 1-3 Order records depends on its zone.

There are three zones: Red, Green and Blue. 'Order' have 5 states:
- 'New', 
- 'To provider', 
- 'Filled', 'Rejected', 'Partially filled'.

Zone distribution:

- Red - only 2-5 states available.
- Green - all 1-5.
- Blue - only 1-2.

More detailed info will be added later.  
 
# Requirements
* Python and packages:
  - python 3.x+
  - pika 1.0.0+
  - mysql-connector-python 8.0.15+
  - protobuf 3.7.1+
* mysql server 8.0
* rabbitmq 3.7.13

# Usage details
1. If app moved to another PC and pathes to settings, log folder etc. is not remote, delete pathes.json to re-initialize it

2. Do not delete root.py - file indicates root of app to all components

3. If settings.json empty or not presented, settings-default.json is used insead

4. If settings.json empty or not presented, settings-default.json is used insead

# How to launch

1. Create MySQL table from file ./init.sql
2. Download required python packages by requirements.txt:
```
pip install -r ./requirements.txt
```
 
 or by command line with pip:

* Windows

```
pip install mysql-connector-python
pip install pika
pip install protobuf
```

* Linux

```
sudo pip3 install mysql-connector-python
sudo pip3 install pika
sudo pip3 install protobuf

or

sudo apt-get install mysql-connector-python
sudo apt-get install pika
sudo apt-get install protobuf
```
3 . Launch by command:
```
python ./Main.py

```
4 . Generation output will be in './out' folder by default. 

5 . You can configure app by provided '.json' files. F.e.:
- control amount of logs/ output data
- connection settings to services
- log output
- etc.  

#Settings

```
Pathes config'pathes.json' by default. 
This file generates automatically after first launch.
Primary loaded file. Delete only if you want to reconfigure it. 

{
    "DEFAULT_SETTINGS": {
        "is_remote": false,
        "location": "D:\\...\\orders_generator\\settings-default.json"
    },
    "GEN_OUT": {
        "is_remote": false,
        "location": "D:\\...\\orders_generator\\out"
    },
    ...
}

```
```
Common settings.

{
    "logging": { 
        "logger_files_max": 10, 
        "loggers": [ ------------------> You can create 
                                         your own logger by this config 
            {
                "destination": "",
                "is_enabled": true,
                "log_level": 6, -------> 1-7: Fatal-Trace
                "type": "console" -----> Now awailable only 'console', 
                                         'folder', and 'file' types
            },
            {
                "destination": "../log",
                "is_enabled": true,
                "log_level": 6,
                "type": "folder"
            },
            {
                "destination": "../loq/out.txt",
                "is_enabled": false,
                "log_level": 7,
                "type": "file"
            }
        ]
    },
    "mysql": {
        "database": "test",
        "host": "127.0.0.1",
        "keep_connection_open": false,
        "order_table": "order_records",
        "password": "root",
        "port": "3306",
        "user": "root"
    },
    "rabbit": {
        "cache_message_lifetime": 10,
        "enable_cache": false,
        "exchange": "",
        "host": "localhost",
        "mysql_table": "order_notes_rabbit",
        "routing_key": "order_notes"
    },
    "system": {
        "limited_therads": false, ---> NYI
        "out_files_max": 10,
        "threads_max": 10
    }
}
```

Generators settings - 'gen-settings.json'. Here you can change parameters
to generate different data. 

Feel free to modify app)