import datetime
from src.config.config import *


class MessageLimiter:
    message_limit = config['message_limiter']['limit']
    timer_span = config['message_limiter']['time_span']
    messages = []

    @staticmethod
    def handle_message_sent():
        MessageLimiter.messages.append(datetime.datetime.now())

    @staticmethod
    def available_messages_count():
        if len(MessageLimiter.messages) == 0:
            return MessageLimiter.message_limit
        MessageLimiter.messages = [element for element in MessageLimiter.messages
                         if (datetime.datetime.now() - element).total_seconds() < MessageLimiter.timer_span]
        return MessageLimiter.message_limit - len(MessageLimiter.messages)
