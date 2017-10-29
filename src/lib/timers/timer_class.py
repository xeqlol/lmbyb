from src.lib.timers.timer_headers import *
from src.lib.functions_general import *
from src.lib.functions_utils import *
import time


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
