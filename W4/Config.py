import random, re, math

class Config:
    minNumber = math.pow(10, -31)
    maxNumber = math.pow(10, 31)

    @staticmethod
    def GenerateStreamOfRandomNumbers():
        random.seed(0)

        randomNumberStream = []
        for item in range(0, 10000):
            randomNumber = random.randint(0, 10000) / 10000
            randomNumberStream.append(randomNumber)
        return randomNumberStream

    @staticmethod
    def Close(point, origin, range):
        return math.fabs(math.fabs(((point - origin) / point))) < range

