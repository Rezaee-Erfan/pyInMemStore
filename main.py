import ast
from enum import Enum

import pyinmem


class Command(Enum):
    """Enum representing the different commands that can be executed."""
    SET = "SET"
    GET = "GET"
    DELETE = "DELETE"
    SET_EXPIRY = "SET_EXPIRY"
    GET_EXPIRY = "GET_EXPIRY"
    EXIT = "EXIT"


def parse_command(input_string):
    """
    Parse a command from the input string.

    Parameters:
    input_string (str): The input string containing the command.

    Returns:
    cmd (str): The command to execute.
    key (str): The key to operate on.
    args (list): The arguments for the command.
    error (str): An error message if the command is invalid, otherwise None.
    """
    command_parts = input_string.split(" ")
    if len(command_parts) < 2:
        return None, None, "Invalid command"
    cmd, key = command_parts[0], command_parts[1]
    if cmd not in Command.__members__:
        return None, None, "Invalid command"
    return cmd, key, command_parts[2:], None


def main():
    """
    Main function to execute the command loop.
    """
    database = pyinmem.MemStore()
    cursor = pyinmem.Cursor(database)

    try:
        while True:
            cmd, key, args, error = parse_command(input("Enter command: "))
            if error:
                print(error)
                continue

            if cmd == Command.SET.value:
                if len(args) < 1:
                    print("Invalid command")
                    continue
                value = ast.literal_eval(" ".join(args))
                cursor.set(key, value)
            elif cmd == Command.GET.value:
                print(cursor.get(key))
            elif cmd == Command.DELETE.value:
                cursor.delete(key)
            elif cmd == Command.SET_EXPIRY.value:
                if len(args) < 1:
                    print("Invalid command")
                    continue
                cursor.set_expiry(key, int(args[0]))
            elif cmd == Command.GET_EXPIRY.value:
                print(cursor.get_expiry(key))
            elif cmd == Command.EXIT.value:
                break
            cursor.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        database.make_backup()


if __name__ == "__main__":
    """Execute the main function if the script is run directly."""
    main()
