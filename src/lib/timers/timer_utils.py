from src.lib.console import *
from src.lib.functions_utils import *
from src.lib.timers.timer_headers import *


class Timer():
    def __init__(self, irc, channel, timer_name):
        self.irc = irc
        self.channel = channel
        self.timer_name = timer_name
        self.interval = timers[timer_name]['interval']

    def run(self):
        time.sleep(self.interval)
        while True:
            pbot('[timer] %s' % self.timer_name, self.channel)
            self.irc.send_message(self.channel, pass_to_function('timer', self.timer_name, None))
            time.sleep(self.interval)
