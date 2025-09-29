from dataclasses import dataclass
from typing import Callable
import os

TOOL_FUNCS: dict[str, Callable[[dict], dict]] = {}
TOOLS = []

@dataclass
class ToolParameter:
    name: str
    type: str
    description: str
    required: bool = True

def define_function_tool(
    function_name: str,
    description: str,
    tool_func: Callable[[dict], dict],
    parameters: list[ToolParameter]
):
    TOOL_FUNCS[function_name] = tool_func
    TOOLS.append({
        'type': 'function',
        'name': function_name,
        'description': description,
        'parameters': {
            'type': 'object',
            'properties': {
                param.name: {
                    'name': param.name,
                    'description': param.description
                }
                for param in parameters
            },
            'required': [param.name for param in parameters if param.required == True]
        }
    })

def read_file(args):
    file_path = args['file_path']
    file_content = None
    with open(file_path, 'r') as file:
        lines = file.readlines()
        file_content = '\n'.join(lines)
    return { 'file_content': file_content }

def list_directory(args):
    path = args.get('path', '.')
    files = []
    folders = []
    for item_path in os.listdir(path):
        full_path = os.path.join(path, item_path)
        if os.path.isfile(full_path):
            files.append(full_path)
        else:
            folders.append(full_path)
    return {
        'files': files,
        'folders': folders,
    }

def init():
    define_function_tool(
        'read_file',
        "Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names.",
        read_file,
        [
            ToolParameter(
                name='file_path',
                type='string',
                description='Relative file path of the file to read'
            )
        ]
    )
    define_function_tool(
        'list_directory',
        "List files and directories at a given path. If no path is provided, lists files in the current directory.",
        list_directory,
        [
            ToolParameter(
                name='path',
                type='string',
                description='Optional relative path to list files from. Defaults to current directory if not provided.',
                required=False
            )
        ]
    )
