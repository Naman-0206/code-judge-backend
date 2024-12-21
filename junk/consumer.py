import pika
import time
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


queue_name = 'task_queue'
channel.queue_declare(queue=queue_name, durable=True)

sample_event_c = {
    "job_id": 1,
    "lang": "cpp",
    "source_code": """
#include <stdio.h>

int main() {
    int a, b, c;
    scanf("%d", &a);
    scanf("%d", &b);
    scanf("%d", &c);
    printf("%d\\n%d\\n%d\\n", a, b, c);
    return 0;
}
""",
    "time_limit": 5,  # in seconds
    "memory_limit": 512,  # in MB
    "input": "1\n5\n3",
    "expected_output": "1\n5\n3",
}

def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")
    time.sleep(2)
    print("Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
