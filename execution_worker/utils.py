import os
from typing import Tuple
from execution_worker.models import ExecutionEvent


def run_command(command: str, timeout: int = 5, memory_limit: int = 512) -> int:
    """
    Executes a shell command with time and memory limits.

    Args:
        command (str): The shell command to execute.
        timeout (int): The time limit for the command execution in seconds (default: 5).
        memory_limit (int): The memory limit for the command execution in MB (default: 512).

    Returns:
        int: The exit code of the executed command.
        
    Notes:
        - The function uses `prlimit` to enforce memory limits and `timeout` to enforce execution time limits.
        - The `exit_code` is derived by dividing the return value of `os.system` by 256, 
          which accounts for shell exit codes.

    Raises:
        ValueError: If the command is an empty string.
    """
    if not command.strip():
        raise ValueError("Command cannot be an empty string.")

    memorylimit_command = f"prlimit --as={memory_limit * 1024 * 1024} {command}"
    timelimit_command = f"timeout {timeout}s {memorylimit_command}"

    exit_code = os.system(timelimit_command)

    return exit_code // 256


def compare_files(executed_output_file: str, expected_output_file: str) -> int:
    """
    Compares the contents of two files: the executed output and the expected output.

    Args:
        executed_output_file (str): The file path containing the executed program's output.
        expected_output_file (str): The file path containing the expected output.

    Returns:
        int: 
            - 200: If the contents of the executed output file and expected output file are exactly the same.
            - 201: If the contents are the same when trailing newlines are removed.
            - 400: If the contents do not match.
            - 401: If an error occurs (e.g., file not found or another exception).

    Raises:
        FileNotFoundError: If either of the files is not found.
        Exception: For any other errors that occur while reading or comparing the files.
    
    Notes:
        - The comparison is case-sensitive and considers exact content, including newlines.
        - If the files match except for trailing newlines, a "Presentation Error" (exit code 201) is returned.
        - Any file reading errors or unexpected exceptions will return an exit code of 401.
    """
    try:
        with open(executed_output_file, 'r') as executed_file:
            executed_content = executed_file.read()

        with open(expected_output_file, 'r') as expected_file:
            expected_content = expected_file.read()

        if executed_content == expected_content:
            return 200

        if executed_content.rstrip('\n') == expected_content.rstrip('\n'):
            return 201

        return 400

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return 401
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return 401


def create_files(event: ExecutionEvent, working_dir: str) -> Tuple[str, str, str, str]:
    """
    Creates necessary files for code execution based on the given Event instance.

    Args:
        event (Event): An instance of the Event dataclass containing execution details.
        working_dir (str): The directory where files will be created.

    Returns:
        Tuple[str, str, str, str]: Paths to the created files (source, input, output, error).
    """
    os.makedirs(working_dir, exist_ok=True)

    
    source_file_path = os.path.join(working_dir, f"main{event.file_extension}")
    input_file_path = os.path.join(working_dir, "input.txt")
    output_file_path = os.path.join(working_dir, "output.txt")
    error_file_path = os.path.join(working_dir, "error.txt")

    with open(source_file_path, "w") as source_file:
        source_file.write(event.source_code)

    with open(input_file_path, "w") as input_file:
        input_file.write(event.input)

    open(output_file_path, "w").close()
    open(error_file_path, "w").close()

    return source_file_path, input_file_path, output_file_path, error_file_path
