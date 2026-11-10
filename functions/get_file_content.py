import os
import io
from config import CHAR_LIMIT

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Grabs contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Absolute ath of the root working directory"
                },
                "file_path": {
                    "type": "string",
                    "description": "Relative path of the file from the working directory",
                },
            },
            "required": ["file_path"]
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abspath = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(abspath, file_path))
        valid_target = os.path.commonpath([abspath, target]) == abspath
        if not valid_target:
            raise RuntimeError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target):
            raise RuntimeError(f'Error: File not found or is not a regular file: "{file_path}"')
        with io.open(target) as file:
            contents = file.read(CHAR_LIMIT)
            if file.read(1):
                contents += f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'
            return contents
    except Exception as e:
        return f"Error: {e}"
