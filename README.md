# What is it?
This is simply app created for generate data objects named 'Order Record' and 'Order'.
Primary object is 'Order'. 'Order' can have 1-3 Order records depends on its zone.
   
'Order' can have some of these statuses:
- 'New', 
- 'To provider', 
- 'Filled', 'Rejected', 'Partially filled'.

There are three zones: Red, Green and Blue. Order Records distributes like this:
- <b>Red</b> - only 2-5 states available.
- <b>Green</b> - all 1-5.
- <b>Blue</b> - only 1-2.

Order records have next structure:
* <b>order id</b> - combined with status, it creates unique pair, that identifies order record, format: 20 numbers  
* <b>timestamp</b> - point in time, format - Unix timestamp in miliseconds 
* <b>status</b> - state of order at this time point `1 to 5`
* <b>currency pair</b> - pair of currencies, exmaple :`NZD/USD`
* <b>direction</b> - buy or sell, format: `0 or 1`
* <b>initial/fill price</b> - price of one currency unit, format:`*.*****`
* <b>initial/fill volume</b> - order volume. , format:`******.********`
* <b>tags</b> - random tags
* <b>description</b>

So, as result, we have a bunch of records with random data, distributed in time, that represents
"time slice" with certain amount of records, divided into 3 zones.

After generation, data publishing in 3 RabbitMQ queues, pre-treated by protobuf.  
Then order records consumed to MySQL database(without protobuf).

# Requirements
* Python and packages:
  - python 3.x+
  - pika 1.0.0+
  - mysql-connector-python 8.0.15+
  - protobuf 3.7.1+
* mysql server 8.0
* rabbitmq 3.7.13


# How to install & launch
You can install app by downloading .zip file just there ^ or type HTTPS link in command line in any folder on your PC.
Then you have two ways to run it: native or with Docker.
##Windows
### Docker
How to run with Docker:
1. Download Docker: https://hub.docker.com/editions/community/docker-ce-desktop-windows.
You must sign up before downloading. 
2. During installation choose Linux container option.
3. Goto any folder and put run.bat in there.
4. Run run.bat
5. If you have some problems with database install, execute ./env/sql/init.sql by yourself at the start of program. 

If you still have some questions about Docker, visit https://docs.docker.com/docker-for-windows/install/
### Manual install 
If you don't want to or can't use Docker, follow these steps:  
1. Download and install MySQL Server 8.0+: https://dev.mysql.com/downloads/windows/installer/8.0.html
2. Download and install Erlang otp21.3+: https://www.erlang.org/downloads (for Windows x32, x64)
3. Download and install RabbitMQ 3.7.14+: https://www.rabbitmq.com/download.html (for Windows x32, x64)
4. Download and install Python 3.7+: https://www.python.org/downloads/

4. Create MySQL tables from file .env/sql/init.sql. You can access terminal from cmd, 
just find "MySQL 8.0 Command Line Client" and run it and then execute script via this command line.

5. Change all setting values named `host` in `settings.json` to `localhost`.

6. Download required python packages by requirements.txt. To do this, call command line 
from project folder and type:
```
pip install -r ./requirements.txt
```
7 . In the same place, launch app by command:
```
python ./Main.py
```
8 . You can see progress in your browser: http://localhost:15672 and in MySQL command line:
```
select * from order_records limit 100000;
``` 
If `localhost:15672` does not responding, try to open rabbitmq command line,
and execute this:
```
rabbitmqctrl.exe start_app
rabbitmq-plugins.exe enable rabbitmq_management
```
9 . You can configure app by provided '.json' files. F.e.:
- control amount of logs/ output data
- threads
- generation settings 
- connection settings to services
- etc.  
## Linux
###Docker || Manual installation & run
To install all kind of stuff you need just run `run.sh`,
or `run_manually.sh` if you hate Docker or want to install all packages on Linux.

To access control panels of RabbitMQ and MySQL, type this commands in terminals:
```
 /*RabbitMQ*/ - rabbitmqctrl
 
 /*MySQL*/ - mysql -u root -P3306 -h localhost -p
 /*Don't forget password*/ - Enter password:root
```

Most of things are the same as in Windows:
1. Change all setting values named `host` in `settings.json` to `localhost` if run native.

# Usage details
1. If app moved to another PC and pathes to settings, log folder etc. is not remote, 
delete pathes.json if you have never done this.

2. Feel free to modify app)