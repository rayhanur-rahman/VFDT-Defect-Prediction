# implementation of an entropy sampling

import TestRig, Config, math, random, re

symbols = Config.syms


# process one by one item at a time from a random sequence of symbols.
# note that it works for more than two symbols
# note that currentphase isn't aware of the actual sequence. it doesn't store it.
# it just stores its statistical information at a time which are count of all symbols, mode and number of maximum occurance

def symIncrement(currentPhase, randomInput):
    if randomInput == '?':
        return currentPhase
    count = currentPhase[0]
    if randomInput in count:
        count[randomInput] = count[randomInput] + 1
    else:
        count[randomInput] = 1
    mode = max(count.items(), key=lambda k: k[1])[0]
    most = max(count.items(), key=lambda k: k[1])[1]
    return (count, mode, most)

def symDecrement(currentPhase, randomInput):
    count = currentPhase[0]
    if randomInput in count:
        count[randomInput] = count[randomInput] - 1
    mode = max(count.items(), key=lambda k: k[1])[0]
    most = max(count.items(), key=lambda k: k[1])[1]
    return (count, mode, most)

def symEntropy(currentPhase):
    count = currentPhase[0]
    total = sum(count.values())
    entropy = 0
    base = len(count)
    for item in count:
        p = count[item]/total
        entropy = entropy - p*math.log(p, base)
    return entropy

def testSym():
    currentPhase = [{},0,0]
    for item in symbols:
        currentPhase = symIncrement(currentPhase, item)
    output = symEntropy(currentPhase)
    print("Entropy: " + str(output))
    assert Config.Close(output, .9403, .01)


TestRig.O.k(testSym)