from src.config.config import *

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
