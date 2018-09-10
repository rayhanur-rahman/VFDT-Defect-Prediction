import random, math

# set the seed to 0
random.seed(0)

# generate stream of 10,000 random numbers
def GenerateStreamOfRandomNumbers():
    list = []
    for item in range(0,10000):
        randomNumber = random.randint(0,10000) / 10000
        list.append(randomNumber)
    return list

# sort the sample
def SampleSort(sample):
    sample.sort()
    return sample

# get nth percentile
def GetPercentile(sample, n):
    index = math.floor((n/100)*len(sample))
    return sample[index]

def GetPercentiles(sample, percentileParams):
    percentiles = []
    for item in percentileParams:
        percentiles.append((item, GetPercentile(sample, item)))
    return percentiles

def CompareSampleOnTheBasisOfPercentile(sample1, sample2):
    percentile1 = GetPercentile(sample1, 50)
    percentile2 = GetPercentile(sample2, 50)
    return percentile1 < percentile2

def Close(point, origin, range):
    return math.fabs(math.fabs(((point-origin)/point))) < range


samples = [4,10,15,38,54,57,62,83,100,100,174,190,215,225,233,250,260,270,299,300,306,333,350,375,443,475,525,583,780,1000]

minNumber = math.pow(10, -31)
maxNumber = math.pow(10, 31)

syms = ['y','y','y','y','y','y','y','y','y','n','n','n','n','n']