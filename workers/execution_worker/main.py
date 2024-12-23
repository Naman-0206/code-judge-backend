import json
import shutil
from execution_worker import working_dir
from execution_worker.utils import compare_files, create_files
from execution_worker.executors import lang_runners
from execution_worker.constants import exit_codes
from execution_worker.models import ExecutionEvent
from execution_worker.redis_client import save_result


def execute_code(event: ExecutionEvent):
    source_file_path, input_file_path, output_file_path, error_file_path = create_files(event, working_dir)

    lang = event.lang
    time_limit = event.time_limit
    memory_limit = event.memory_limit

    exit_code = lang_runners[lang](
        source_file_path, input_file_path,
        output_file_path, error_file_path, 
        time_limit, memory_limit
    )  

    output = open(output_file_path, "r").read() 
    errors = open(error_file_path, "r").read()
    
    if exit_code != 0:
        shutil.rmtree(working_dir)
        return exit_code, output, errors

    shutil.rmtree(working_dir)

    return exit_code, output, errors


def handle_error(job_id, exit_code):
    """Handle errors and save the result."""

    verdict = exit_codes.get(exit_code, "Unknown error")
    result = {
        "job_id": job_id,
        "exit_code": exit_code,
        "verdict": verdict,
    }
    return result

def event_callback(ch, method, properties, body):
    job_id = None
    try:
        event = json.loads(body.decode())
        job_id = event["job_id"]
        if job_id is None:
            raise ValueError("job_id is required")
        event = ExecutionEvent(**event)

    except Exception as e:
        print(e)
        if job_id is not None:
            error_msg = handle_error(job_id, 402)
            save_result(job_id, error_msg)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    
    print("Received: ", event.job_id)
    
    try:
        exit_code, output, error = execute_code(event)
        if exit_code not in exit_codes:
            error_msg = handle_error(job_id, 500)
            save_result(job_id, error_msg)
            ch.basic_ack(delivery_tag=method.delivery_tag)    
            return
        
        msg = {
            "job_id": event.job_id,
            "exit_code": exit_code,
            "verdict": exit_codes[exit_code],
            "input": event.input,
            "output": output,
            "error": error
        }
        save_result(event.job_id, msg)
    
    except Exception as e:
        print(e)
        error_msg = handle_error(job_id, 500)   
        save_result(job_id, error_msg) 
        
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)



















# sample_event = {
#     "lang": "c", # c, cpp, python
#     "source_code": "# some code",
#     "time_limit": 5, # in seconds
#     "memory_limit": 512, # in MB
#     "input": "1\n5\n3",
#     "expected_output": "1\n5\n3",
# }

# sample_event_c = {
#     "job_id": 1,
#     "lang": "cpp",
#     "source_code": """
# #include <stdio.h>

# int main() {
#     int a, b, c;
#     scanf("%d", &a);
#     scanf("%d", &b);
#     scanf("%d", &c);
#     printf("%d\\n%d\\n%d\\n", a, b, c);
#     return 0;
# }
# """,
#     "time_limit": 5,  # in seconds
#     "memory_limit": 512,  # in MB
#     "input": "1\n5\n3",
#     "expected_output": "1\n5\n3",
# }

# if __name__ == "__main__":
#     exit_code = execute_code(ExecutionEvent(**sample_event_c))

#     print("Exit Code:", exit_code)
#     print("Verdict:", exit_codes.get(exit_code, "Unknown Error"))
#     print(ExecutionEvent.from_json(json.dumps(sample_event_c)))

    