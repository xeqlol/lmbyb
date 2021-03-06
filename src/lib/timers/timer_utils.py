import _thread
import itertools

from src.lib.console import *
from src.lib.common_utils import *
from src.lib.timers.timer_headers import *
from src.lib.limiter import *


class TimerHandler():
    def __init__(self, irc, config):
        self.irc = irc
        self.config = config

    def handle(self):
        allowed_sequential_timers = []

        for channel in self.config['channels']:
            if channel in self.config['timers']:
                if 'all' in self.config['timers'][channel]['allowed_timers']:
                    allowed_timers = timer_headers
                else:
                    allowed_timers = self.config['timers'][channel]['allowed_timers']

                for timer in allowed_timers:
                    if not timer_headers[timer]['sequential']:
                        _thread.start_new_thread(self.run_non_sequential_timer, (channel, timer))
                    else:
                        allowed_sequential_timers.append(timer)
                if len(allowed_sequential_timers) > 0:
                    _thread.start_new_thread(self.run_sequential_timers, (channel, allowed_sequential_timers))

    def run_non_sequential_timer(self, channel, timer):
        interval = timer_headers[timer]['interval']
        time.sleep(interval)
        while True:
            handle_function(self.irc, timer, channel)
            time.sleep(interval)

    def run_sequential_timers(self, channel, timers):
        pool = itertools.cycle(timers)
        timer = next(pool)
        time.sleep(int(timer_headers[timer]['interval']))
        while True:
            handle_function(self.irc, timer, channel)
            timer = next(pool)
            time.sleep(timer_headers[timer]['interval'])


def handle_function(irc, timer, channel):
    available_message_count = MessageLimiter.available_messages_count()
    if available_message_count > 0:
        pbot('Timer "{0}" is handled. Available messages count: {1}.'.format(timer, available_message_count), channel)
        if check_returns_function('timer', timer):
            message = pass_to_function('timer', timer, None)
        else:
            message = timer_headers[timer]['return']
        irc.send_message(channel, message)
        MessageLimiter.handle_message_sent()