import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to specified file within working directory",
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
                "content": {
                    "type": "string",
                    "description": "The content to be written to File at file_path",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abspath = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(abspath, file_path))
        valid_target = os.path.commonpath([abspath, target]) == abspath
        if not valid_target:
            raise RuntimeError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target):
            raise RuntimeError(f'Error: Cannot write to "{file_path}" as it is a directory')

        parent_path = os.path.dirname(target)
        os.makedirs(parent_path, exist_ok=True)

        with open(target, "w") as f:
            f.write(content)
        with open(target, "r") as f:
            if content in f.read():
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            else:
                return f'Failed to write to "{file_path}"'

    except Exception as e:
        return f"Error: {e}"
