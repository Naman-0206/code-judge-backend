from typing import Callable, Dict
from execution_worker.utils import run_command, time_execution
from execution_worker import working_dir


@time_execution
def execute_python_code(source_file, input_file, output_file, error_file, timeout=5, memory_limit=512):
    
    command = f"python3 {source_file} < {input_file} > {output_file} 2> {error_file}"
    
    return run_command(command, timeout, memory_limit)

@time_execution
def execute_cpp_code(source_file, input_file, output_file, error_file, timeout=5, memory_limit=512):
    
    compile_command = f"g++ {source_file} -o {working_dir}/a.out 2> {error_file}"
    exit_code = run_command(compile_command, timeout, memory_limit)
    
    if exit_code != 0:
        return 125

    command = f"{working_dir}/a.out < {input_file} > {output_file} 2> {error_file}"
    
    return run_command(command, timeout, memory_limit)

@time_execution
def execute_c_code(source_file, input_file, output_file, error_file, timeout=5, memory_limit=512):
    
    compile_command = f"gcc {source_file} -o {working_dir}/a.out 2> {error_file}"
    exit_code = run_command(compile_command, timeout, memory_limit)
    
    if exit_code != 0:
        return 125

    command = f"{working_dir}/a.out < {input_file} > {output_file} 2> {error_file}"
    
    return run_command(command, timeout, memory_limit)

lang_runners: Dict[str, Callable] = {
    "c": execute_c_code,
    "cpp": execute_cpp_code,
    "python": execute_python_code
}

file_extensions = {
    "c": ".c",
    "cpp": ".cpp",
    "python": ".py"
}