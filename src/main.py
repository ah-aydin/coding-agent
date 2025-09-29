from client import GPTClient
import tools

def main():
    tools.init()
    print('Chat with GPT (use ctrl-c to quit)')
    client = GPTClient()
    try:
        while True:
            client.process_user_input()
    except KeyboardInterrupt:
        print("\nGood bye!")

        
if __name__ == '__main__':
    main()
