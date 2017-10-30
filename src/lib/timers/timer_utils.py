import _thread

from src.lib.console import *
from src.lib.functions_utils import *
from src.lib.timers.timer_headers import *


class TimerHandler():
    def __init__(self, irc, config):
        self.irc = irc
        self.config = config

    def handle(self):
        # start threads for channels that have cron messages to run
        # maybe better to move this to bot.py, idk
        for channel in config['channels']:
            allowed_timers = []
            if 'all' in config['timers'][channel]['allowed_timers']:
                allowed_timers = timers
            else:
                allowed_timers = config['timers'][channel]['allowed_timers']

            for timer in allowed_timers:
                _thread.start_new_thread(self.run, (channel, timer))

    def run(self, channel, timer):
        interval = timers[timer]['interval']
        time.sleep(interval)
        while True:
            pbot('[timer] %s' % timer, channel)
            self.irc.send_message(channel, pass_to_function('timer', timer, None))
            time.sleep(interval)