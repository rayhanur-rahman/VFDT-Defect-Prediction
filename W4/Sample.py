import random, re, math, Config


class Sample():
    def __init__(self, maximumSize):
        self.maximumSize = maximumSize
        self.listOfSamples = []
        self.sequence = 0
        self.isSorted = False

    def increment(self, randomInput):
        actualSize = len(self.listOfSamples)
        self.sequence = self.sequence + 1
        if actualSize < self.maximumSize:
            self.listOfSamples.append(randomInput)
        else:
            randomNumber = random.randint(0, self.sequence)
            if randomNumber <= self.maximumSize:
                randomIndex = random.randint(0, self.maximumSize - 1)
                self.listOfSamples[randomIndex] = randomInput
        return

    def sort(self):
        if not self.isSorted:
            self.listOfSamples.sort()
            self.isSorted = True

    def getPercentile(self, n):
        index = math.floor((n / 100) * len(self.listOfSamples))
        return self.listOfSamples[index]

    def getPercentiles(self, percentileParams):
        percentiles = []
        for item in percentileParams:
            percentiles.append((item, self.getPercentile(item)))
        return percentiles
