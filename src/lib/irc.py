import re
import socket
import sys

import src.config.config as config
from src.lib.console import *


class Irc:
    def __init__(self, config):
        self.config = config

    def check_for_message(self, b_message):
        message = b_message.decode('utf-8')
        if message[0] == '@' and 'PRIVMSG' in message:
            arg_regx = "([^=;]*)=([^ ;]*)"
            arg_regx = re.compile(arg_regx, re.UNICODE)
            args = dict(re.findall(arg_regx, message[1:]))
            regex = ('^@[^ ]* :([^!]*)![^!]*@[^.]*.tmi.twitch.tv'  # username
                     ' PRIVMSG #([^ ]*)'  # channel
                     ' :(.*)')  # message
            regex = re.compile(regex, re.UNICODE)
            match = re.search(regex, message)
            return True
        return False

    def check_is_command(self, message, valid_commands):
        for command in valid_commands:
            if command == message:
                return True

    def check_for_connected(self, data):
        if re.match(r'^:.+ 001 .+ :connected to TMI$', data):
            return True

    def check_for_ping(self, data):
        if data[:4] == "PING":
            self.sock.send('PONG')

    def get_message(self, data):
        return {
            'channel': re.findall(r'PRIVMSG (.*?) :', data.decode('utf-8'))[0],
            'username': re.findall(r'display-name=(.*?);', data.decode('utf-8'))[0],
            'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data.decode('utf-8'))[0],
            # not sure that 'in' faster than regex, gonna find out
            'is_broadcaster': True if 'broadcaster/1' in  data.decode('utf-8') else False,
            'is_moderator': True if 'moderator/1' in  data.decode('utf-8') else False,
            'is_subscriber': True if 'subscriber=1' in data.decode('utf-8') else False,
        }

    def check_login_status(self, data):
        if re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data.decode('utf-8')):
            return False
        else:
            return True

    def send_message(self, channel, message):
        if config.config['me_mod']:
            message = '/me %s' % message
        self.sock.send(bytes('PRIVMSG %s :%s\n' % (channel, message), 'utf-8'))

    def get_irc_socket_object(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        self.sock = sock

        try:
            sock.connect((self.config['server'], self.config['port']))
        except:
            pp('Cannot connect to server (%s:%s).' % (self.config['server'], self.config['port']), 'error')
            sys.exit()

        sock.settimeout(None)

        sock.send(bytes('USER %s\r\n' % self.config['username'], 'utf-8'))
        sock.send(bytes('PASS %s\r\n' % self.config['oauth_password'], 'utf-8'))
        sock.send(bytes('NICK %s\r\n' % self.config['username'], 'utf-8'))

        if self.check_login_status(sock.recv(1024)):
            pp('Login successful.')
        else:
            pp('Login unsuccessful. (hint: make sure your oauth token is set in self.config/self.config.py).', 'error')
            sys.exit()

        self.join_channels(self.channels_to_string(self.config['channels']))
        self.set_cap_requests()

        return sock

    def channels_to_string(self, channel_list):
        return ','.join(channel_list)

    def join_channels(self, channels):
        pp('Joining channels %s.' % channels)
        self.sock.send(bytes('JOIN %s\r\n' % channels, 'utf-8'))
        pp('Joined channels.')

    def leave_channels(self, channels):
        pp('Leaving chanels %s,' % channels)
        self.sock.send(bytes('PART %s\r\n' % channels, 'utf-8'))
        pp('Left channels.')

    def set_cap_requests(self):
        if self.config['cap_reqs']['membership']:
            self.sock.send(bytes('CAP REQ :twitch.tv/membership\r\n', 'utf-8'))
            pp('Request for membership')
        if self.config['cap_reqs']['tags']:
            self.sock.send(bytes('CAP REQ :twitch.tv/tags\r\n', 'utf-8'))
            pp('Request for tags')
        if self.config['cap_reqs']['commands']:
            self.sock.send(bytes('CAP REQ :twitch.tv/commands\r\n', 'utf-8'))
            pp('Request for commands')
