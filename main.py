import commands
import os
import json

def main():
    commands.select_campaign()

    while True:
        command = input("Enter a command: ")
        command_parts = command.split()

        if command_parts[0].lower() == "help":
            commands.help()
        elif hasattr(commands, command_parts[0]) and callable(getattr(commands, command_parts[0])):
            try:
                getattr(commands, command_parts[0])(*command_parts[1:])
            except TypeError:
                print("Error: Incorrect number of arguments.")
            except Exception as e:
                print(f"Error: {e}")
        elif command_parts[0].lower() == "exit":
            break
        else:
            print("Invalid command. Type 'Help' for available commands.")

if __name__ == "__main__":
    main()
