import src.lib.functions_utils as commands
from src.lib.timers.timer_utils import *


class CommandHandler():
    def __init__(self, irc, config):
        self.irc = irc
        self.config = config
        self.sock = irc.get_irc_socket_object()

    def handle(self):
        while True:
            data = self.sock.recv(config['socket_buffer_size']).rstrip()

            if len(data) == 0:
                pp('Connection was lost, reconnecting.')
                sock = self.irc.get_irc_socket_object()

            if config['debug']:
                print('debug: %s' % data)

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
                if commands.is_valid_command(message) or commands.is_valid_command(message.split(' ')[0]):
                    command = message

                    if commands.check_returns_function(command.split(' ')[0]):
                        if commands.check_has_correct_args(command, command.split(' ')[0]):
                            args = command.split(' ')
                            del args[0]

                            command = command.split(' ')[0]

                            if commands.is_on_cooldown(command, channel):
                                pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                                    command, username, commands.get_cooldown_remaining(command, channel)),
                                     channel
                                     )
                            else:
                                pbot('Command is valid an not on cooldown. (%s) (%s)' % (
                                    command, username),
                                     channel
                                     )

                                result = commands.pass_to_function('command', command, args)
                                commands.update_last_used(command, channel)

                                if result:
                                    resp = '@%s > %s' % (username, result)
                                    pbot(resp, channel)
                                    self.irc.send_message(channel, resp)

                    else:
                        if commands.is_on_cooldown(command, channel):
                            pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                                command, username, commands.get_cooldown_remaining(command, channel)),
                                 channel
                                 )
                        elif commands.check_has_return(command):
                            pbot('Command is valid and not on cooldown. (%s) (%s)' % (
                                command, username),
                                 channel
                                 )
                            commands.update_last_used(command, channel)

                            resp = '@%s > %s' % (username, commands.get_return(command))
                            commands.update_last_used(command, channel)

                            pbot(resp, channel)
                            self.irc.send_message(channel, resp)


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
