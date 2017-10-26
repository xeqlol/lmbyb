import src


# one of defaults bot's commands
def commands():
    available_commands = ', '.join(str(command) for command in src.lib.commands._command_headers.command_headers)
    return 'Available commands: %s' % available_commands
