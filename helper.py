import time
import json


def realitycheck(bot):
    """

    :param bot: tBot
    """
    checks = [
        '''13.06.2016 10:44 :~: Einmal Popcorn bitte. 50 Liter.

        Reality
        Ich höre: "Forever alone"

        Story
        Ich habe eine Szene aus Indiana Jones und der Tempel des Todes im Kopf und denke: "Die Insekten lassen dich niemals allein."''',

        '''02.06.2016 20:52 :~: Saudi Arabi Money Rich

        Reality
        Ich lese auf Twitter: "Haftbefehl gegen mutmaßlichen IS-Terroristen."

        Story
        Ich frage mich, was mehr Terror bedeutet. So eine kleine Explosion oder 3:28 Gesinge von Chabos und Babos?''',

        '''13.02.2016 17:54 :~: Die Stange war zu kurz

        Reality
        Eine neue Person betritt den Raum. Bewaffnet mit Hut und Heißklebepistole läuft sie zielstrebig auf jemanden zu. Dieser ist allerdings nicht zu Gesprächen aufgelegt...
        Story
        ... und sagt: "Gib mal kurz!", schnappt sich die Heißklebepistole, hält sie sich an die Schläfe und drückt ab.'''
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