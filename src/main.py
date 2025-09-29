from client import GPTClient

def print_GPT(text):
    print(f'\u001b[93mGPT\u001b[0m: {text}\n', end='')


def main():
    print('Chat with GPT (use ctrl-c to quit)')

    client = GPTClient()
    try:
        while True:
            client.process_user_input()
    except KeyboardInterrupt:
        print("\nGood bye!")

        
if __name__ == '__main__':
    main()
