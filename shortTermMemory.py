import time


class shortTermMemory(object):
    def __init__(self):
        self.memoryList = []
        self.autoClean = True

    def add(self, data, timeToLive=0):
        if self.autoClean:
            self.clean()

        self.memoryList.append(memory(data, timeToLive))

    def isInMemory(self, data):
        if self.autoClean:
            self.clean()

        for memory in self.memoryList:
            if memory.data == data:
                return True
        return False

    def clean(self, maxAge=120):
        currentTime = time.time()
        for memory in reversed(self.memoryList):
            if maxAge > 0 and memory.time + maxAge < currentTime:
                #print('OLD AGE:' + memory.data)
                self.memoryList.remove(memory)
            elif memory.removeMe():
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
    stm.clean(4)
    stm.clean()

