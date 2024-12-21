import subprocess

# Find the full path of python3
python_path = subprocess.run(["which", "python3"], capture_output=True, text=True)
print(f"Python 3 executable found at: {python_path.stdout.strip()}")

# Now run the python --version command with the full path
cmd = subprocess.run([python_path.stdout.strip(), "--version"], capture_output=True, text=True)

# Print the output and any errors
print(f"STDOUT: {cmd.stdout}")
print(f"STDERR: {cmd.stderr}")
