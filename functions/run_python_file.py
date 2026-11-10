import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs python code",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Absolute path of the root working directory",
                },
                "file_path": {
                    "type": "string",
                    "description": "Relative path of the file from the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Arguments to pass to the script. Omit or leave empty if none"
                },
            },
            "required": ["file_path"]
        },
    }
}

def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abspath = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(abspath, file_path))
        valid_target = os.path.commonpath([abspath, target]) == abspath
        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target]

        if args:
            for arg in args:
                command.append(arg)

        try:
            sub = subprocess.run(command, cwd=abspath, capture_output=True, text=True, timeout=30)
            output = ""
            if sub.returncode != 0:
                output += f"Process exited with code {sub.returncode}\n"
            if not sub.stdout and not sub.stderr:
                output += "No output produced\n"
            if sub.stdout:
                output += f"STDOUT: {sub.stdout}\n"
            if sub.stderr:
                output += f"STDERR: {sub.stderr}\n"
            return output
        except Exception as e:
            return f"Error: executing Python file: {e}"


    except Exception as e:
        return f"Error: {e}"
