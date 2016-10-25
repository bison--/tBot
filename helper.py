import time
import json


def realitycheck(bot):
    """

    :param bot: tBot
    """
    checks = [
        '''13.06.2016 10:44 :~: Einmal Popcorn bitte. 50 Liter. http://realitycheck.pl/search/?q=Einmal+Popcorn+bitte.+50+Liter."''',
        '''02.06.2016 20:52 :~: Saudi Arabi Money Rich http://realitycheck.pl/search/?q=Saudi+Arabi+Money+Rich''',
        '''13.02.2016 17:54 :~: Die Stange war zu kurz http://realitycheck.pl/search/?q=Die+Stange+war+zu+kurz''',
        '10.08.2016 15:09 :~: Artikelnummer 3 oder 0 http://realitycheck.pl/search/?q=Artikelnummer+3+oder+0'
    ]
    import random
    for line in random.choice(checks).split("\n"):
        bot.chat(line)


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