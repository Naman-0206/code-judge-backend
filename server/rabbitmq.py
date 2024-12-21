import json
import pika
import sys
import time
from redis_client import r

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'remotecodeexecution-rabbitmq-1',
                                                               heartbeat=30))
channel = connection.channel()

submit_queue = 'task_queue'
channel.queue_declare(queue=submit_queue, durable=True)

execution_queue = 'execution_queue'
channel.queue_declare(queue=execution_queue, durable=True)



























sample_event_c = {
    # "job_id": 1,
    # "lang": "cpp",
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

# for i in range(100):

#     print(f"Sending: {i}")
#     message = json.dumps({"job_id":i, **sample_event_c})

    # channel.basic_publish(
    #         exchange='',
    #         routing_key=queue_name,
    #         body=message,
    #         properties=pika.BasicProperties(
    #             delivery_mode=2,  # Make the message persistent
    #         )
    #     )

# connection.close()
# s = list(range(100))
# while s:
#     for i in s:
#         res = r.get(i)
#         if res: 
#             print(i, res)
#             s.remove(i)
#     time.sleep(1)

# while r.get(1500) is None: time.sleep(1)

# print(1500, r.get(1500))