from openai import OpenAI
import tools
import json

MODEL='gpt-3.5-turbo'

TOOLS = [
    tools.define_function_tool(
        'get_weather',
        'Get the weather of a given city',
        [
            tools.ToolParameter(name='city', type='string', description='The city for which to check the weather for', required=False)
        ]
    )
]

class GPTClient:
    def __init__(self):
        self.client = OpenAI()
        self.conversation = []

    def process_user_input(self):
        print('\u001b[94mYou\u001b[0m: ', end='')
        user_input = input()

        self.conversation.append({'role': 'user', 'content': user_input})
        response = self.client.responses.create(
            model=MODEL,
            input=self.conversation,
            tools=TOOLS,
            store=False
        )

        self.conversation += response.output
        for item in response.output:
            if item.type == 'function_call':
                if item.name == 'get_weather':
                    weather = tools.get_weather(json.loads(item.arguments))
                    self.conversation.append({
                        'type': 'function_call_output',
                        'call_id': item.call_id,
                        'output': json.dumps({
                            'weather': weather
                        })
                    })
                    tool_response = self.client.responses.create(
                        model=MODEL,
                        tools=TOOLS,
                        instructions='Respond with the response that you got from the tool about the weather of the city.',
                        input=self.conversation,
                        store=False
                    )
                    self.__print_GPT(tool_response.output_text)
                continue
            model_output = response.output_text
            self.__print_GPT(model_output)

    def __print_GPT(self, text):
        print(f'\u001b[93mGPT\u001b[0m: {text}\n', end='')
