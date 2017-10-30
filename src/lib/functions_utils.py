import importlib
import time

from src.lib.commands.command_headers import *
from src.lib.timers.timer_headers import *


def is_valid_command(command):
    if command in command_headers:
        return True


def update_last_used(command, channel):
    command_headers[command][channel]['last_used'] = time.time()


def get_command_limit(command):
    return command_headers[command]['limit']


def is_on_cooldown(command, channel):
    if time.time() - command_headers[command][channel]['last_used'] < command_headers[command]['limit']:
        return True


def get_cooldown_remaining(command, channel):
    return round(command_headers[command]['limit'] - (time.time() - command_headers[command][channel]['last_used']))


def check_has_return(command):
    if command_headers[command]['return'] and command_headers[command]['return'] != 'command':
        return True


def get_return(command):
    return command_headers[command]['return']


def check_has_args(command):
    if 'argc' in command_headers[command]:
        return True


def check_has_correct_args(message, command):
    message = message.split(' ')
    if len(message) - 1 == command_headers[command]['argc']:
        return True


def check_returns_function(type, function):
    if type == 'command':
        _dict = command_headers
    elif type == 'timer':
        _dict = timer_headers
    if _dict[function]['return'] == 'function':
        return True
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
