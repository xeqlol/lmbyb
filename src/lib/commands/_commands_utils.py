def access_level(message_dict):
    level = 0
    if message_dict['is_subscriber']:
        level = 1
    if message_dict['is_moderator']:
        level = 2
    if message_dict['is_broadcaster']:
        level = 3
    return level
