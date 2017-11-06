import time

red = "\033[01;31m{0}\033[00m"
grn = "\033[01;32m{0}\033[00m"
ylw = "\033[01;33m{0}\033[00m"
blu = "\033[01;34m{0}\033[00m"


def pp(message, mtype='INFO'):
    mtype = mtype.upper()
    if mtype == 'ERROR':
        mtype = red.format(mtype)
    else:
        mtype = blu.format(mtype)

    print('[{0}] [{1}] {2}'.format(time.strftime('%H:%M:%S', time.gmtime()), mtype, message))


def ppi(channel, message, username):
    print(
        '[{0} {1}] <{2}> {3}'.format(time.strftime('%H:%M:%S', time.gmtime()), channel, grn.format(username.lower()), message))


def pbot(message, channel=''):
    if channel:
        msg = '[{0} {1}] <{2}> {3}'.format(time.strftime('%H:%M:%S', time.gmtime()), channel, ylw.format('BOT'), message)
    else:
        msg = '[{0}] <{1}> {2}'.format(time.strftime('%H:%M:%S', time.gmtime()), ylw.format('BOT'), message)

    print(msg)
