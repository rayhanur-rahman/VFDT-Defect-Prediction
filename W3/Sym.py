import Config, math, random, re

class Sym:
    def __init__(self, title, columnIndex):
        self.frequency = {}
        self.total = 0
        self.mode = None
        self.most = None
        self.title = title
        self.status = None
        self.isClass = None
        self.columnIndex = columnIndex

    def increment(self, randomInput):
        if randomInput == '?':
            return
        if randomInput in self.frequency:
            self.frequency[randomInput] = self.frequency[randomInput] + 1
        else:
            self.frequency[randomInput] = 1
        self.mode = max(self.frequency.items(), key=lambda k: k[1])[0]
        self.most = max(self.frequency.items(), key=lambda k: k[1])[1]
        self.total = self.total + 1
        return

    def decrement(self, randomInput):
        if randomInput == '?':
            return
        if randomInput in self.frequency:
            self.frequency[randomInput] = self.frequency[randomInput] - 1
        self.mode = max(self.frequency.items(), key=lambda k: k[1])[0]
        self.most = max(self.frequency.items(), key=lambda k: k[1])[1]
        self.total = self.total - 1


    def getEntropy(self):
        entropy = 0
        base = len(self.frequency)
        for item in self.frequency:
            p = self.frequency[item] / self.total
            entropy = entropy - p * math.log(p, base)

        return entropy