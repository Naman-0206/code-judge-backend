import pika
import logging
import aiopika
from aiopika import connect_robust
logger = logging.getLogger(__name__)


class PikaClient:
    def __init__(self, publish_queue_name, process_callable):
        self.publish_queue_name = publish_queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=env('RABBITMQ_HOST', '127.0.0.1'))
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(
            queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable
        logger.info('Pika connection initialized')


async def consume(self, loop):
    """Setup message listener with the current running loop"""
    connection = await connect_robust(host=env('RABBITMQ_HOST', '127.0.0.1'),
                                      port=5672,
                                      loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue(env('CONSUME_QUEUE', 'foo_consume_queue'))
    await queue.consume(self.process_incoming_message, no_ack=False)
    logger.info('Established pika async listener')
    return connection


async def process_incoming_message(self, message):
    """Processing incoming message from RabbitMQ"""
    message.ack()
    body = message.body
    logger.info('Received message')
    if body:
        self.process_callable(json.loads(body))


def send_message(self, message: dict):
    """Method to publish message to RabbitMQ"""
    self.channel.basic_publish(
        exchange='',
        routing_key=self.publish_queue_name,
        properties=pika.BasicProperties(
            reply_to=self.callback_queue,
            correlation_id=str(uuid.uuid4())
        ),
        body=json.dumps(message)
    )
