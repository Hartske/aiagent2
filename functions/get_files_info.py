import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abspath = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abspath, directory))
        valid_target_dir = os.path.commonpath([abspath,target_dir]) == abspath
        if not valid_target_dir:
            raise RuntimeError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            raise RuntimeError(f'Error: "{directory}" is not a directory')
        
        contents = []

        with os.scandir(target_dir) as entries:
            for entry in entries:
                try:
                    contents.append(f"- {entry.name}: file_size={entry.stat().st_size}, is_dir={entry.is_dir()}")
                except Exception as er:
                    return f"Error: {er}"

        result = "\n".join(contents)
        return result

    except Exception as e:
        return f"Error: {e}"
