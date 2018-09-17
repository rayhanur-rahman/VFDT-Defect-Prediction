import Config, math


class Num:
    def __init__(self, title, columnIndex):
        self.mean = 0
        self.variance = 0
        self.sd = 0
        self.count = 0
        self.min = 0
        self.max = 0
        self.listOfSamples = []
        self.title = title
        self.goal = None
        self.status = None
        self.columnIndex = columnIndex

    def increment(self, randomInput):
        if randomInput == '?':
            return
        self.count = self.count + 1
        d = (randomInput - self.mean)
        self.mean = self.mean + d / (self.count)
        self.variance = self.variance + d * (randomInput - self.mean)
        self.sd = math.sqrt(
            math.fabs(self.variance) / (self.count - 1 + Config.Config.minNumber)) if self.count >= 2 else 0
        self.min = randomInput if randomInput < self.min else self.min
        self.max = randomInput if randomInput > self.max else self.max
        return

    def decrement(self, randomInput):
        if self.count == 1 or randomInput == '?':
            return
        self.count = self.count - 1
        d = (randomInput - self.mean)
        self.mean = self.mean - d / self.count
        self.variance = self.variance - d * (randomInput - self.mean)
        self.sd = math.sqrt(
            math.fabs(self.variance) / (self.count - 1 + Config.Config.minNumber)) if self.count >= 2 else 0
        self.min = randomInput if randomInput < self.min else self.min
        self.max = randomInput if randomInput > self.max else self.max
        return

    def getNormalizedValue(self, input):
        return (input - self.min) / (self.max - self.min + Config.Config.minNumber)

    def getExpectedValue(self, anotherNum):
        n = self.count + anotherNum.count + Config.Config.minNumber
        return (self.sd * self.count + anotherNum.sd * anotherNum.count) / n
