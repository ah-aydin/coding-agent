from dataclasses import dataclass

@dataclass
class ToolParameter:
    name: str
    type: str
    description: str
    required: bool

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

def get_weather(city):
    return f'The weather in ${city} is 28 degrees'
