import json
import shutil
from submission_worker import working_dir
from submission_worker.utils import compare_files, create_files
from submission_worker.executors import lang_runners
from submission_worker.constants import exit_codes
from submission_worker.models import Event
from submission_worker.redis_client import save_result


def execute_code(event: Event):
    source_file_path, input_file_path, output_file_path, expected_output_file_path, error_file_path = create_files(event, working_dir)

    lang = event.lang
    time_limit = event.time_limit
    memory_limit = event.memory_limit

    exit_code = lang_runners[lang](
        source_file_path, input_file_path,
        output_file_path, error_file_path, 
        time_limit, memory_limit
    )   
    
    if exit_code != 0:
        shutil.rmtree(working_dir)
        return exit_code

    exit_code = compare_files(output_file_path, expected_output_file_path)

    shutil.rmtree(working_dir)

    return exit_code



def event_callback(ch, method, properties, body):
    job_id = None
    try:
        event = json.loads(body.decode())
        job_id = event["job_id"]
        if job_id is None:
            raise ValueError("job_id is required")
        event = Event(**event)
    except Exception as e:
        print(e)
        if job_id is not None:
            save_result(job_id, exit_codes[402])
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    
    print("Received: ", event.job_id)
    save_result(event.job_id, "Running...")
    
    try:
        exit_code = execute_code(event)
        if exit_code not in exit_codes:
            save_result(event.job_id, "Unknown error")
            return
        save_result(event.job_id, exit_codes[exit_code])
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    except Exception as e:
        print(e)
        save_result(event.job_id, "Unknown error")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return


sample_event = {
    "lang": "c", # c, cpp, python
    "source_code": "# some code",
    "time_limit": 5, # in seconds
    "memory_limit": 512, # in MB
    "input": "1\n5\n3",
    "expected_output": "1\n5\n3",
}

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

if __name__ == "__main__":
    exit_code = execute_code(Event(**sample_event_c))

    print("Exit Code:", exit_code)
    print("Verdict:", exit_codes.get(exit_code, "Unknown Error"))
    print(Event.from_json(json.dumps(sample_event_c)))

    