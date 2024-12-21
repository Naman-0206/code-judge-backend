import json
import pika
import sys
import time

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue (it will be created if it doesn't exist)
queue_name = 'task_queue'
channel.queue_declare(queue=queue_name, durable=True)

# Send messages to the queue
# for i in range(1, 6):  # sending 5 tasks
#     message = f"Task {i}"
#     channel.basic_publish(
#         exchange='',
#         routing_key=queue_name,
#         body=message,
#         properties=pika.BasicProperties(
#             delivery_mode=2,  # Make the message persistent
#         )
#     )
#     print(f"Sent: {message}")
#     time.sleep(1)  # Simulate a delay between task submissions


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


channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(sample_event_c),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        )
    )
# Close the connection
connection.close()
