import time


class shortTermMemory(object):
    def __init__(self):
        self.memoryList = []
        self.autoClean = True

    def add(self, data, timeToLive=0):
        '''
        :param data: text/data to check for (counts as a key)
        :param timeToLive: remember this for X seconds
        :return: None
        '''
        if self.autoClean:
            self.clean()

        self.memoryList.append(memory(data, timeToLive))

    def addUpdate(self, data, timeToLive=0):
        if self.isInMemory(data):
            self.setTimeFor(data, timeToLive)
        else:
            self.add(data, timeToLive)

    def setTimeFor(self, data, timeToLive):
        found = 0
        for memory in reversed(self.memoryList):
            if memory.data == data:
                memory.setNewTime(timeToLive)
                found += 1
        return found

    def isInMemory(self, data):
        if self.autoClean:
            self.clean()

        for memory in self.memoryList:
            if memory.data == data:
                return True
        return False

    def getFromMemory(self, data):
        """
        to get equals overloaded data from memory
        :param data:
        :return: None or object
        """
        if self.autoClean:
            self.clean()

        for memory in self.memoryList:
            if memory.data == data:
                return memory
        return None

    def clean(self, enforce=False):
        if enforce:
            self.memoryList.clear()
        else:
            currentTime = time.time()
            for memory in reversed(self.memoryList):
                if memory.removeMe():
                    self.memoryList.remove(memory)
                else:
                    #print('IN TIME:' + memory.data)
                    pass

    def clear(self):
        self.memoryList = []


class memory(object):
    def __init__(self, data, timeToLive):
        self.time = time.time()
        self.data = data
        self.timeToLive = timeToLive

    def setNewTime(self, timeToLive):
        self.time = time.time()
        self.timeToLive = timeToLive

    def removeMe(self):
        if self.timeToLive == 0:
            return False
        elif self.time + self.timeToLive < time.time():
            return True
        else:
            return False


if __name__ == "__main__":
    stm = shortTermMemory()
    stm.add('test')
    time.sleep(1)
    stm.clean()
    stm.add('test2')
    time.sleep(5)
    stm.add('test3')
    stm.clean()
