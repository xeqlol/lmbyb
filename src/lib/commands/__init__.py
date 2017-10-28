import os
import glob

__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+'/*.py')]

from src.config.config import *
from src.lib.commands._command_headers import command_headers

commands = command_headers

for channel in config['channels']:
    for command in command_headers:
        commands[command][channel] = {}
        commands[command][channel]['last_used'] = 0