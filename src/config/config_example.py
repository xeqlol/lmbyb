global config


config = {

    # details required to login to twitch IRC server
    'server': 'irc.chat.twitch.tv',
    'port': 6667,
    'username': 'botname',
    'oauth_password': 'oauth:youroauth',  # get this from http://twitchapps.com/tmi/

    # adds /me at the start of response
    'me_mod': True,

    # channel to join
    'channels': ['#channel'],

    # list of timers
    'timers': {
        '#channel': {
            'allowed_timers': 'all' # or list of allowed timers
        }
    },

    # list of admins
    'admins': {
        'admin'
    },

    # cap request strings
    'cap_reqs': {
        'membership': True,
        'tags': True,
        'commands': True
    },
    # if set to true will display any data received
    'debug': True,

    # if set to true will log all messages from all channels
    # todo
    'log_messages': False,

    # maximum amount of bytes to receive from socket - 1024-4096 recommended
    'socket_buffer_size': 2048
}
