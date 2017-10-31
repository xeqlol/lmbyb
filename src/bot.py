import src.lib.irc as irc_
from src.lib.commands.command_utils import *
from src.lib.timers.timer_utils import *


class Bot:
    def __init__(self, config):
        self.config = config
        self.irc = irc_.Irc(config)

    def run(self):
        TimerHandler(self.irc, self.config).handle()
        CommandHandler(self.irc, self.config).handle()