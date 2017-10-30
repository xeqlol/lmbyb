from src.lib.commands.command_headers import *


# one of defaults bot's commands
def commands():
    available_commands = ', '.join(str(command) for command in command_headers)
    return 'Available commands: %s' % available_commands
