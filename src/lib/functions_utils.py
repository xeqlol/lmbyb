# todo: move commands function to commands folder, fimers function to timers folder
import time
from src.lib.commands import *

import importlib


def is_valid_command(command):
    if command in commands:
        return True


def update_last_used(command, channel):
    commands[command][channel]['last_used'] = time.time()


def get_command_limit(command):
    return commands[command]['limit']


def is_on_cooldown(command, channel):
    if time.time() - commands[command][channel]['last_used'] < commands[command]['limit']:
        return True


def get_cooldown_remaining(command, channel):
    return round(commands[command]['limit'] - (time.time() - commands[command][channel]['last_used']))


def check_has_return(command):
    if commands[command]['return'] and commands[command]['return'] != 'command':
        return True


def get_return(command):
    return commands[command]['return']


def check_has_args(command):
    if 'argc' in commands[command]:
        return True


def check_has_correct_args(message, command):
    message = message.split(' ')
    if len(message) - 1 == commands[command]['argc']:
        return True


def check_returns_function(command):
    if commands[command]['return'] == 'function':
        return True


# todo: separate commands and timers functions
def pass_to_function(type, function, args):
    if type == 'command':
        command = function.replace('!', '')
        module = importlib.import_module('src.lib.commands.%s' % command)
        function = getattr(module, command)

    elif type == 'timer':
        module = importlib.import_module('src.lib.timers.%s' % function)
        function = getattr(module, function)

    if args:
        return function(args)
    else:
        return function()
