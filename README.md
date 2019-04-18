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

# How to launch

## Docker
```yml
docker image pull rabbitmq:3.7.14-management-alpine
docker image pull python:3.7.3-alpine3.9
docker image pull mysql:8.0

docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 localnet
docker-compose up
docker network inspect localnet - get host for services here
docker build -t order_gen .
docker run -it --network localnet order_gen
```

1. Create MySQL tables from file ./init.sql
2. Download required python packages by requirements.txt:
```
pip install -r ./requirements.txt
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


1. Pathes config'pathes.json' by default. 
This file generates automatically after first launch.
Primary loaded file. Delete only if you want to reconfigure it. 

```
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
2 . Common settings. Lots of options here.
```


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

3 . Generators settings - 'gen-settings.json'. Here you can change parameters
to generate different data. 

Feel free to modify app)