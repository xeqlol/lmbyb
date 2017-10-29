global config


config = {

    # details required to login to twitch IRC server
    'server': 'irc.chat.twitch.tv',
    'port': 6667,
    'username': 'bot_name',
    'oauth_password': 'oauth:your_oauth',  # get this from http://twitchapps.com/tmi/

    # adds /me at the start of response
    'me_mod': True,

    # channel to join
    'channels': ['#channel'],

    'cron': {
        '#channel': {
            'run_cron': False,
            # set this to false if you want don't want to run the cronjob but you want to preserve the messages etc
            'run_time': 120,  # time in seconds
            'cron_messages': [
                'This is #channel cron message one.',
                'This is #channel cron message two.'
            ]
        }
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
    'log_messages': True,

    # maximum amount of bytes to receive from socket - 1024-4096 recommended
    'socket_buffer_size': 2048
}
