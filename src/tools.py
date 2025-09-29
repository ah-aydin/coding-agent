from dataclasses import dataclass

@dataclass
class ToolParameter:
    name: str
    type: str
    description: str
    required: bool = True

def define_function_tool(
        function_name: str,
        description: str,
        parameters: list[ToolParameter]
):
    return {
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
    }

TOOLS = [
    define_function_tool(
        'get_weather',
        'Get the weather of a given city',
        [
            ToolParameter(name='city', type='string', description='The city for which to check the weather for', required=False)
        ]
    ),
    define_function_tool(
        'read_file',
        "Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names.",
        [
            ToolParameter(name='file_path', type='string', description='Relative file path of the file to read')
        ]
    )
]

def get_weather(city):
    return f'The weather in ${city} is 28 degrees'

def read_file(args):
    print('The arguments to read_file are:', args)
    file_path = args['file_path']
    file_content = None
    with open(file_path, 'r') as file:
        lines = file.readlines()
        file_content = '\n'.join(lines)
    return file_content

