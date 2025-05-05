import pika
from logging import getLogger
from .service import event_callback
import os

logger = getLogger(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    os.getenv("RABBITMQ_HOST"), os.getenv("RABBITMQ_PORT")))
channel = connection.channel()

queue_name = 'submission_queue'
channel.queue_declare(queue=queue_name, durable=True)

# Ensures one message is processed at a time
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=event_callback)

logger.info("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()

