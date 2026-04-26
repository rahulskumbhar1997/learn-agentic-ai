from agent import Agent
from tools import Calculator, Registry, Weather

def interactive_mode():

    while True:

        command = str(input("> "))
        if command.lower() == "exit":
            break
        if command.lower() == "":
            continue

        agent.run(user_input=command)

if __name__ == "__main__":

    registry = Registry()
    registry.register(Calculator())
    registry.register(Weather())
    agent = Agent(tool_registry=registry)
    # agent.run(user_input="What is capital of India. Answer in one line.")
    interactive_mode()
    