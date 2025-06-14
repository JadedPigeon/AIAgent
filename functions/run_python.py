import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_filepath = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_filepath.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_filepath):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_directory
        )

        if not result.stdout.strip() and not result.stderr.strip():
            return "No output produced."

        output = ""
        if result.stdout.strip():
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr.strip():
            output += f"\nSTDERR:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"

        return output.strip()

    except Exception as e:
        return f'Error: executing Python file: {e}'
