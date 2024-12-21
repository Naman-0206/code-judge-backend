from pathlib import Path
import shutil
import subprocess

extensions = {
    "cpp": "cpp",
    "c": "c",
    "java": "java",
    "python3": "py",
}

def createFiles(body):
    current_dir = Path.cwd()
    
    temp_path = current_dir / "temp"
    temp_path.mkdir(exist_ok=True)

    folder_path = temp_path / body['jobId']
    folder_path.mkdir(exist_ok=True)
    
    input_file = folder_path / "input.txt"
    source_file = folder_path / f"source.{extensions[body['lang']]}"
    output_path = folder_path / "output.txt"
    logs_file = folder_path / "logs.txt"
    error_file = folder_path / "error.txt"

    
    input_file.write_text(body["input"], encoding="utf-8")
    source_file.write_text(body["src"], encoding="utf-8")
    output_path.touch()
    logs_file.touch()
    error_file.touch()

    return folder_path, output_path , logs_file, error_file
def executeCode(body):
    try:
        folder_path, output_path, logs_file, error_file = createFiles(body)
        python_path = subprocess.run(["which", "python3"], capture_output=True, text=True).stdout.strip()

        # command for container
        command = f"python runner.py ../temp/{body['jobId']}/source.{extensions[body['lang']]} {body['lang']} {body['timeOut']}".split()
        # command = f"python ./worker/runner.py ./temp/{body['jobId']}/source.{extensions[body['lang']]} {body['lang']}"
        # command = "ls"
        # command = f"runner.py"
        result = subprocess.run(command, capture_output=True, text=True, timeout=int(body["timeOut"]))
        
        print(result.stdout)
        print(result.stderr)
        with open(logs_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
        
        with open(error_file, "w", encoding="utf-8") as f:
            f.write(result.stderr)

        shutil.rmtree(folder_path, ignore_errors=True)

    except Exception as e:
        # TODO : error handling
        print(e)
        pass
        

def test():
    body = {
        "jobId" : "123",
        "lang" : "python3",
        "input" : "Hello World",
        "src" : "print(input())",
        "timeOut" : 1
    }
    executeCode(body)


if __name__ == "__main__":
    test()