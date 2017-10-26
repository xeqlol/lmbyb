import random, json


def randomemote():
    filename = 'src/res/global_emotes.json'

    try:
        data = json.loads(open(filename, 'r').read())
    except:
        return 'Error reading %s.' % filename

    emote = random.choice(list(data.keys()))

    return '%s = %s' % (
        emote,
        emote[:1] + '​' + emote[1:]
    )