import pika
from execution_worker.main import event_callback
from logging import getLogger
import os

logger = getLogger(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.getenv("RABBITMQ_HOST"), 
    port=os.getenv("RABBITMQ_PORT"),
    virtual_host=os.getenv("RABBITMQ_VHOST", "/"),
    credentials=pika.PlainCredentials(
        os.getenv("RABBITMQ_USER", "guest"),
        os.getenv("RABBITMQ_PASSWORD", "guest")
    )))

channel = connection.channel()

queue_name = 'execution_queue'
channel.queue_declare(queue=queue_name, durable=True)

# Ensures one message is processed at a time
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=event_callback)

logger.info("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
