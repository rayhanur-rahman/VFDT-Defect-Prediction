# this is the implementation of reservoir sampling
import TestRig, Config, random, math

# create six samples, these will have the capacity of 32, 64, 128, 256, 512 and 1024
def createSamples():
    samples = []

    for i in range(4, 11):
        samples.append([[], 0, math.pow(2, i)])

    return samples # return samples with sampled item processed so far and maximum size limit

# process one input at a time
# for a sample size n, from the random sequence copy first n numbers exactly
# then for the rest of the sequence, replace one of the existing item with the new random
# number with decreasing probability of size/total items processed from the sequence so far
def sampleIncrement(sample, randomInput):
    maxSize = sample[2]
    actualSize = len(sample[0])
    sample[1] = sample[1] + 1
    sequence = sample[1]

    if actualSize < maxSize:
        sample[0].append(randomInput)
    else:
        randomNumber = random.randint(0, sequence)
        if randomNumber <= maxSize:
            randomIndex = random.randint(0, maxSize - 1)
            sample[0][randomIndex] = randomInput
    return sample

streamOfRandomNumbers = Config.GenerateStreamOfRandomNumbers()

def testSample():
    sample = createSamples()

    print("Size:\t50th Percentile")

    for item in sample:
        for randomNumber in streamOfRandomNumbers:
            sampleIncrement(item, randomNumber)
        Config.SampleSort(item[0])
        percentile = Config.GetPercentile(item[0], 50)
        print( str(int(item[2])) + ": \t" + str(percentile))
        assert Config.Close(percentile, 0.5, 0.33) == True


TestRig.O.k(testSample)