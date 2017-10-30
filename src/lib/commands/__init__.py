from src.config.config import *
from src.lib.commands.command_headers import *
from src.lib.commands.functions import *


for channel in config['channels']:
    for command in command_headers:
        command_headers[command][channel] = {}
        command_headers[command][channel]['last_used'] = 0