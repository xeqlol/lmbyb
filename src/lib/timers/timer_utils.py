import _thread
import itertools

from src.lib.console import *
from src.lib.common_utils import *
from src.lib.timers.timer_headers import *


class TimerHandler():
    def __init__(self, irc, config):
        self.irc = irc
        self.config = config

    def handle(self):
        allowed_sequential_timers = []

        for channel in self.config['channels']:
            allowed_timers = []
            if 'all' in self.config['timers'][channel]['allowed_timers']:
                allowed_timers = timer_headers
            else:
                allowed_timers = self.config['timers'][channel]['allowed_timers']

            for timer in allowed_timers:
                if not allowed_timers[timer]['sequential']:
                    _thread.start_new_thread(self.run, (channel, timer))
                else:
                    allowed_sequential_timers.append(timer)
            if len(allowed_sequential_timers) > 0:
                _thread.start_new_thread(self.run_sequential_timers, (channel, allowed_sequential_timers))

    def run(self, channel, timer):
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
    pbot('[timer] %s' % timer, channel)
    if check_returns_function('timer', timer):
        message = pass_to_function('timer', timer, None)
    else:
        message = timer_headers[timer]['return']
    irc.send_message(channel, message)