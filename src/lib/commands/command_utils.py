import src.lib.common_utils as commands

from src.lib.timers.timer_utils import *


class CommandHandler():
    def __init__(self, irc, config):
        self.irc = irc
        self.config = config
        self.sock = irc.get_irc_socket_object()

    def handle(self):
        while True:
            data = self.sock.recv(self.config['socket_buffer_size']).rstrip()

            if len(data) == 0:
                pp('Connection was lost, reconnecting.')
                sock = self.irc.get_irc_socket_object()

            if self.config['debug']:
                print('debug: {0}'.format(data))

            # check for ping, reply with pong
            self.irc.check_for_ping(data)

            if self.irc.check_for_message(data):
                message_dict = self.irc.get_message(data)

                channel = message_dict['channel']
                message = message_dict['message']
                username = message_dict['username']

                # make access levels for commands
                print(access_level(message_dict))

                ppi(channel, message, username)

                # check if message is a command with no arguments
                if is_valid_command(message) or is_valid_command(message.split(' ')[0]):
                    command = message
                    available_message_count = MessageLimiter.available_messages_count()
                    if available_message_count > 0:
                        if check_returns_function('command', command.split(' ')[0]):
                            if check_has_correct_args(command, command.split(' ')[0]):
                                args = command.split(' ')
                                del args[0]

                                command = command.split(' ')[0]

                                if is_on_cooldown(command, channel):
                                    pbot('Command "{0}" from {1} is on cooldown. ({2}s remaining)'.format(
                                        command, username, get_cooldown_remaining(command, channel)),
                                         channel
                                         )
                                else:
                                    pbot('Command "{0}" from {1} is valid and not on cooldown. Available messages count: {2}'.format(
                                        command, username, available_message_count),
                                         channel
                                         )

                                    result = commands.pass_to_function('command', command, args)
                                    update_last_used(command, channel)

                                    if result:
                                        resp = '@{0} > {1}'.format(username, result)
                                        pbot(resp, channel)
                                        self.irc.send_message(channel, resp)
                                        MessageLimiter.handle_message_sent()

                        else:
                            if is_on_cooldown(command, channel):
                                pbot('Command "{0}" from {1} is on cooldown. ({2}s remaining)'.format(
                                    command, username, get_cooldown_remaining(command, channel)),
                                     channel
                                     )
                            elif check_has_return(command):
                                pbot('Command "{0}" from {1} is valid and not on cooldown. Available messages count: {2}'.format(
                                    command, username, available_message_count),
                                     channel
                                     )
                                update_last_used(command, channel)

                                resp = '@{0} > {1}'.format(username, get_return(command))
                                update_last_used(command, channel)

                                pbot(resp, channel)
                                self.irc.send_message(channel, resp)
                                MessageLimiter.handle_message_sent()


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

def access_level(message_dict):
    level = 0
    if message_dict['is_subscriber']:
        level = 1
    if message_dict['is_moderator']:
        level = 2
    if message_dict['is_broadcaster']:
        level = 3
    if message_dict['username'] in config['admins']:
        level = 9000 # OVER 9000!!!!1111
    return level
