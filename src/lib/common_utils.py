import importlib

from src.lib.commands.command_headers import *
from src.lib.timers.timer_headers import *


def check_returns_function(type, function):
    if type == 'command':
        return command_headers[function]['return'] == 'function'
    elif type == 'timer':
        return timer_headers[function]['return'] == 'function'
    else:
        return False

# todo: separate commands and timers functions
def pass_to_function(type, function, args):
    if type == 'command':
        command = function.replace('!', '')
        module = importlib.import_module('src.lib.commands.functions.%s' % command)
        function = getattr(module, command)

    elif type == 'timer':
        module = importlib.import_module('src.lib.timers.functions.%s' % function)
        function = getattr(module, function)

    if args:
        return function(args)
    else:
        return function()
