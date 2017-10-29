import os
import glob
from src.config.config import *
from src.lib.commands.command_headers import *


__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+'/*.py')]

for channel in config['channels']:
    for command in commands:
        commands[command][channel] = {}
        commands[command][channel]['last_used'] = 0