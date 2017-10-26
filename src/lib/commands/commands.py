import src


def commands():
    available_commands = ', '.join(str(command) for command in src.lib.commands.__command_headers.command_headers)
    return 'Available commands: %s' % available_commands
