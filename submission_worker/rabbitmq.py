import pika
from submission_worker.main import event_callback
from logging import getLogger

logger = getLogger(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters('remotecodeexecution-rabbitmq-1'))
channel = connection.channel()

queue_name = 'task_queue'
channel.queue_declare(queue=queue_name, durable=True)

channel.basic_qos(prefetch_count=1)  # Ensures one message is processed at a time
channel.basic_consume(queue=queue_name, on_message_callback=event_callback)

logger.info("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
