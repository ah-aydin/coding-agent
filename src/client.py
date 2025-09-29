from openai import OpenAI
import tools
from tools import TOOLS
import json

MODEL='gpt-3.5-turbo'

class GPTClient:
    def __init__(self):
        self.client = OpenAI()
        self.conversation = []

    def process_user_input(self):
        response = self._send_user_input()
        had_tool_calls = False
        for item in response.output:
            if item.type == 'function_call':
                had_tool_calls = True
                if item.name == 'get_weather':
                    weather = tools.get_weather(json.loads(item.arguments))
                    self.conversation.append({
                        'type': 'function_call_output',
                        'call_id': item.call_id,
                        'output': json.dumps({
                            'weather': weather
                        })
                    })
                continue
            model_output = response.output_text
            self._print_GPT(model_output)

        if had_tool_calls:
            tool_response = self._get_tool_call_response('Respond with the response that you got from the tool about the weather of the city.')
            self._print_GPT(tool_response.output_text)

    def _send_user_input(self):
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
        return response

    def _get_tool_call_response(self, instructions: str):
        return self.client.responses.create(
            model=MODEL,
            tools=TOOLS,
            instructions=instructions,
            input=self.conversation,
            store=False
        )



    def _print_GPT(self, text):
        print(f'\u001b[93mGPT\u001b[0m: {text}\n', end='')
