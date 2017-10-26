from src.config.config import *
from src.lib.commands._command_headers import command_headers

commands = command_headers

for channel in config['channels']:
    for command in command_headers:
        commands[command][channel] = {}
        commands[command][channel]['last_used'] = 0