import pika
from _redis import redis_client
import os
import logging
from pika.exceptions import AMQPChannelError

logger = logging.getLogger(__name__)

import pika
import os

class RabbitMQ:
    def __init__(self):
        self.user = os.getenv('RABBITMQ_USER', 'guest')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials, heartbeat=30)
        # self.connection = pika.BlockingConnection(parameters)
        self.connection = pika.SelectConnection(parameters)
        self.channel = self.connection.channel()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def consume(self, queue_name, callback):
        if not self.channel:
            raise Exception("Connection is not established.")
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def publish(self, queue_name, message):
        # try:
        if self.channel.is_closed or self.connection.is_closed:
            self.close()
            self.connect()
            logger.info("rabbitmq reconnected")
            raise Exception("Connection is not established.")
        
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(exchange='',
                                routing_key=queue_name,
                                body=message,
                                properties=pika.BasicProperties(
                                    delivery_mode=2,  # make message persistent
                                ))
        print(f"Sent message to queue {queue_name}: {message}")
        # except Exception as e:
        #     logger.error(f"Error publishing message to queue {queue_name}: {e}")
        #     logger.info(f"{self.channel, self.connection}")


class RabbitMQ():
    def __init__(self):
        self.user = os.getenv('RABBITMQ_USER', 'guest')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials, heartbeat=30)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
    
    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def publish(self, queue_name, message):
        try:
            self.connect()
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.basic_publish(exchange='',
                                    routing_key=queue_name,
                                    body=message,
                                    properties=pika.BasicProperties(
                                        delivery_mode=2,  # make message persistent
                                    ))
            print(f"Sent message to queue {queue_name}: {message}")
            self.close()
        except Exception as e:
            logger.error(f"Error publishing message to queue {queue_name}: {e}")

rabbit = RabbitMQ()

