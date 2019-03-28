




def declare_queue(channel, key):
    channel.queue_declare(queue=key)


def send_messages(connection, exchange, routing_key, messages):
    for message in messages:
        send_message(connection, exchange, routing_key, message, False)
    close_connection(connection)


def send_message(connection, exchange, routing_key, message, close_after_sending=True):
    connection.channel().basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    if close_after_sending:
        close_connection(connection)


def dummy_callback(ch, method, properties, body):
    x = 0


def consume_messages(channel, routing_key, callback=dummy_callback):
    channel.basic_consume(callback, queue=routing_key, no_ack=True)
    channel.start_consuming()
