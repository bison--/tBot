import random


class randomList(object):
    def __init__(self):
        self.elements = [
        ]

        self.remainingElements = []

    def getElement(self):
        if len(self.remainingElements) == 0:
            self.remainingElements = list(self.elements)

        index = random.randint(0, len(self.remainingElements) - 1)
        selectedElement = self.remainingElements[index]
        self.remainingElements.remove(selectedElement)

        return selectedElement

    def loadFromDict(self, _dict, loadKeys = True):
        entries = []
        if loadKeys:
            entries = _dict.keys()
        else:
            entries = _dict.values()

        for entry in entries:
            if not entry in self.elements:
                self.elements.append(entry)


if __name__ == "__main__":
    rl = randomList()

    rl.elements = [
        'https://www.youtube.com/watch?v=OxSiQG5AnA8',
        'https://www.youtube.com/watch?v=jsdawgd0azk',
        'https://www.youtube.com/watch?v=XMCYNH1EJTg',
        'https://www.youtube.com/watch?v=dXw6UWJV1dU',
        'https://www.youtube.com/watch?v=tP7vRAr79N0',
        'https://www.youtube.com/watch?v=vJUvrw7O_6I',
        'https://www.youtube.com/watch?v=tDTQQWSmo8s',
        'https://www.youtube.com/watch?v=Vj41xZHA5Eg',
        'https://www.youtube.com/watch?v=KmqgRAXygDg',
        'https://www.youtube.com/watch?v=1mjlM_RnsVE',
        'https://www.youtube.com/watch?v=11CKOAQDsbg',
        'https://www.youtube.com/watch?v=d5P5Tz3VH94',
        'https://www.youtube.com/watch?v=f_9g2nXpYl0'
    ]

    print(rl.remainingElements)
    print(rl.getElement())
    print(rl.remainingElements)
    print(rl.getElement())
    print(rl.remainingElements)