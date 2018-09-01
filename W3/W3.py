import TestRig, random, math

streamOfRandomNumbers = []

def GenerateStreamOfRandomNumbers():
    list = []
    for item in range(0,10000):
        randomNumber = random.randint(0,10000) / 10000
        list.append(randomNumber)
    return list

streamOfRandomNumbers = GenerateStreamOfRandomNumbers()

def reservoirSampler(streamOfRandomNumbers, size):
    reservoir = []
    for item in range(0, size):
        reservoir.append(streamOfRandomNumbers[item])

    for item in range(size, len(streamOfRandomNumbers)):
        randomNumber = random.randint(0, len(streamOfRandomNumbers))
        if randomNumber > size:
            randomIndex = random.randint(0, size-1)
            reservoir[randomIndex] = streamOfRandomNumbers[item]

    reservoir.sort()
    return reservoir

def getPercentile(list, n):
    index = math.floor((n/100)*len(list))
    return list[index]

def close(point, origin, range):
    return math.fabs(math.fabs(((point-origin)/point)) - range)

def testReservoirSampler():
    for item in range(1,10):
        list = []
        reservoir = reservoirSampler(streamOfRandomNumbers, int(math.pow(2, item)))
        percentile = getPercentile(reservoir, 50)
        assert close(percentile, .5, .25) < .25

TestRig.O.k(testReservoirSampler)

samples = [4,10,15,38,54,57,62,83,100,100,174,190,215,225,233,250,260,270,299,300,306,333,350,375,443,475,525,583,780,1000]

def ComputeMuAndSdOnline(currentPhase, newValue):
    mean = currentPhase[0] + (newValue - currentPhase[0])/(currentPhase[2]+1)
    sd = currentPhase[1] + (newValue - currentPhase[0])*(newValue - mean)
    count = currentPhase[2]+1
    return (mean, sd, count)

def testMuAndSd():
    currentPhase = [0,0,0]
    for index in range(0,len(samples)):
        currentPhase = ComputeMuAndSdOnline(currentPhase, samples[index])
    assert currentPhase[0] == 270.3 and close(math.sqrt(currentPhase[1]/(len(samples)-1)), 231.946, .001)

TestRig.O.k(testMuAndSd)



