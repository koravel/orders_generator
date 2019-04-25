sudo apt install python3-pip

pip install -r ./requirements.txt

sudo apt install erlang
sudo apt install rabbitmq-server
rabbitmq-plugins enable rabbitmq_management

sudo apt-get install mysql-server
sudo mysql_secure_installation

python3 ./Main.py
