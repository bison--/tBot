import time
import json


DURATION_IGNORE = -1
DURATION_MINUTES_1 = 60
DURATION_MINUTES_2 = 120
DURATION_MINUTES_30 = DURATION_MINUTES_1 * 30
DURATION_HOURS_1 = 3600
DURATION_HOURS_2 = DURATION_HOURS_1 * 2
DURATION_HOURS_4 = DURATION_HOURS_1 * 4


def realitycheck(bot):
    """

    :param bot: tBot
    """
    checks = [
        '29. Juni 2020 08:43 :~: Das Who is Who im Schlachtbetrieb https://realitycheck.pl/post/das-who-is-who-im-schlachtbetr',
        '30. Juli 2019 16:04 :~: Ist das Schild vegan? https://realitycheck.pl/post/ist-das-schild-vegan''',
        '31. Mai 2019 08:49 :~: Das mach ich mit links (die Hand ist flacher) https://realitycheck.pl/post/das-mach-ich-mit-links-die-han',
        '9. März 2019 08:51 :~: Leider ungenügend https://realitycheck.pl/post/leider-ungenugend'
    ]

    import random
    bot.chat(random.choice(checks))


def explainHamster(bot):
    """

    :param bot: tBot
    """
    bot.chat("HAMSTER sind im grunde genau wie Zigaretten...")
    time.sleep(1.5)
    bot.chat("Vollkommen harmlos... bis man sie sich in den Mund steckt und anzündet!")
    time.sleep(1.5)


def getReadableTime(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d h %02d m %02d s" % (h, m, s)


def saveJson(file, data):
    try:
        with open(file, 'w') as data_file:
            json.dump(data, data_file)
    except Exception as ex:
        print(ex)


def loadJson(file):
    data = None
    try:
        with open(file) as data_file:
            data = json.load(data_file)
    except Exception as ex:
        print(ex)

    return data


def log(msg):
    """
    :type msg: string
    """
    print(time.strftime("%Y-%m-%d %H:%M:%S: ") + msg)


def popGiveAway():
    allLines = open('../giveAways.txt', 'r').readlines()
    newLines = ''
    returnLine = ''
    for line in allLines:
        line = line.strip()
        if returnLine == '' and line != '' and line[0] != '#':
            returnLine = line
            newLines += '#' + line + "\n"
        elif line != '':
            newLines += line + "\n"

    writeHandle = open('../giveAways.txt', 'w')
    writeHandle.write(newLines)
    writeHandle.close()
    #print(allLines)
    return returnLine


def dictToChat(_dict):
    msg = ''
    for key, value in _dict.items():
        msg += '{}: {}, '.format(key, value)

    return msg.strip(', ')
