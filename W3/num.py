import TestRig, Config, math, random, re

samples = Config.samples

# currentphase tuple contains mu, m2, sd, count, min, max of a given sequence of number
# note that currentphase isn't aware of the actual sequence. it doesn't store it.
# it just stores its statistical information at a time

def numIncrement(currentPhase, randomInput):
    if randomInput == '?':
        return currentPhase
    mean = currentPhase[0] + (randomInput - currentPhase[0]) / (currentPhase[3] + 1)
    var = currentPhase[1] + (randomInput - currentPhase[0]) * (randomInput - mean)
    count = currentPhase[3] + 1
    sd = math.sqrt(var/(count - 1 + Config.minNumber)) if count >= 2 else 0
    min = randomInput if randomInput < currentPhase[4] else currentPhase[4]
    max = randomInput if randomInput > currentPhase[5] else currentPhase[5]
    return (mean, var, sd, count, min, max)

def numDecrement(currentPhase, randomInput):
    if randomInput == '?':
        return currentPhase
    mean = currentPhase[0] - (randomInput - currentPhase[0]) / (currentPhase[3] + 1)
    var = currentPhase[1] - (randomInput - currentPhase[0]) * (randomInput - mean)
    count = currentPhase[3] - 1
    sd = math.sqrt(var/(count - 1 + Config.minNumber)) if count >= 2 else 0
    min = randomInput if randomInput < currentPhase[4] else currentPhase[4]
    max = randomInput if randomInput > currentPhase[5] else currentPhase[5]
    return (mean, var, sd, count, min, max)

def getNormalizedValue(currentPhase, input):
    min = currentPhase[4]
    max = currentPhase[5]
    return (input - min)/(max - min + Config.minNumber)

def getExpectedValue(currentPhase1, currentPhase2):
    n = currentPhase1[3] + currentPhase2[3] + Config.minNumber
    return (currentPhase1[2]*currentPhase1[3] + currentPhase2[2]*currentPhase2[3])/n

def testNum():
    currentPhase = [0,0,0,0,0,0]
    for index in range(0,len(samples)):
        currentPhase = numIncrement(currentPhase, samples[index])
    print("(means, variance, sd, total, min, max)")
    print(currentPhase)
    assert currentPhase[0] == 270.3 and Config.Close(currentPhase[2], 231.946, .01)

TestRig.O.k(testNum)