from openai import OpenAI
import tools
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
                tool_args = json.loads(item.arguments)
                print(f'\n\u001b[92mtool\u001b[0m: {item.name}({tool_args})\n')
                # tool_output = tools.TOOLS.(item.name).func(tool_args)
                tool = tools.TOOL_FUNCS.get(item.name)
                if tool is None:
                    continue
                tool_output = tool(tool_args)
                self.conversation.append({
                    'type': 'function_call_output',
                    'call_id': item.call_id,
                    'output': json.dumps(tool_output)
                })
            model_output = response.output_text
            self._print_GPT(model_output)

        if had_tool_calls:
            tool_response = self._get_tool_call_response('Response do the input that you got from the user with the information from the tool calls you\'ve made')
            self._print_GPT(tool_response.output_text)

    def _send_user_input(self):
        print('\u001b[94mYou\u001b[0m: ', end='')
        user_input = input()

        self.conversation.append({'role': 'user', 'content': user_input})
        response = self.client.responses.create(
            model=MODEL,
            input=self.conversation,
            tools=tools.TOOLS,
            store=False
        )
        self.conversation += response.output
        return response

    def _get_tool_call_response(self, instructions: str):
        return self.client.responses.create(
            model=MODEL,
            tools=tools.TOOLS,
            instructions=instructions,
            input=self.conversation,
            store=False
        )



    def _print_GPT(self, text):
        if len(text) < 1: return
        print(f'\u001b[93mGPT\u001b[0m: {text}\n', end='')
