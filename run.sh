sudo apt install docker.io
rabbitmq-plugins enable rabbitmq_management
docker pull koravel/orders_generator:latest
docker-compose up