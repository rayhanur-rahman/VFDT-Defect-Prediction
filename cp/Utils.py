import csv, re, Utils, Num, Sym, math, sys


def retrieveSet(data, attributeName):
    list = []
    for item in data:
        list.append(item[attributeName])
    return set(list)

def getType(item):
    match = re.match(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$', item)
    if match:
        return "num"
    match = re.match(r'^[ _a-zA-Z_]+[a-zA-Z0-9 _]*$', item)
    if match:
        return "str"
    return "none"

def csvRowsGenerator(csvfile):
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            yield row

def getDiscretizedRange(data, attribute):
    list = []
    for item in data:
        list.append(item[attribute])
    cuts = []
    cutIndexs = []
    list.sort()
    enough = math.pow(len(list), 0.5)
    queue = []
    indexQueue = []
    queue.append(list)
    indexQueue.append(0)
    discretizedData = []

    while len(queue) != 0:
        poppedItem = queue.pop(0)
        poppedIndex = indexQueue.pop(0)
        low = 0
        high = len(poppedItem)
        min = sys.maxsize
        max = -sys.maxsize
        num1 = Num.Num("", None)
        num2 = Num.Num("", None)
        for item in poppedItem:
            num1.increment(item)
        best = num1.sd
        cutIndex = None
        count = 0
        for item in poppedItem:
            num1.decrement(item)
            num2.increment(item)
            if num1.count >= math.ceil(enough) and num2.count >= math.ceil(enough):
                expectedValueOfSd = num1.getExpectedValue(num2) * 1.05
                if expectedValueOfSd < best:
                    cutIndex = count
                    best = expectedValueOfSd
            count = count + 1
        if cutIndex is not None:
            cuts.append(poppedItem[cutIndex])
            cutIndexs.append(poppedIndex + cutIndex)
            list1 = []
            list2 = []
            for index in range(0, len(poppedItem)):
                if index <= cutIndex:
                    list1.append(poppedItem[index])
                else:
                    list2.append(poppedItem[index])

            if len(list1) > 0:
                queue.append(list1)
                indexQueue.append(poppedIndex)
            if len(list2) > 0:
                queue.append(list2)
                indexQueue.append(cutIndex+1)


    cuts.sort()
    cutIndexs.sort()
    # print(cutIndexs)
    minRange = []
    maxRange = []
    cutIndex = 0
    listIndex  = 0
    minIndex = 0
    for item in list:
        if item == cuts[cutIndex]:
            minRange.append(list[minIndex])
            maxRange.append(cuts[cutIndex])
            cutIndex = cutIndex + 1
            minIndex = listIndex + 1
            if cutIndex == len(cuts):
                break
        listIndex = listIndex + 1
    if maxRange[-1] is not list[-1]:
        minRange.append(list[minIndex])
        maxRange.append(list[-1])
    # print(f'---  {cuts} {minRange} {maxRange}')
    return minRange, maxRange, cuts

def getFromSetByIndex(set, index):
    count = 0
    for item in set:
        if count is index:
            return item
        count = count + 1
    return


def getBestSplitNumeric(list, attributeName):
    list.sort(key=lambda k: k[attributeName])
    unique = Utils.retrieveSet(list, 'class')
    ranges = Utils.getDiscretizedRange(list, attributeName)

    totalMatrix = [0] * len(unique)
    for itemIndex in list:
        for index in range(0, len(unique)):
            if itemIndex['class'] == Utils.getFromSetByIndex(unique, index):
                totalMatrix[index] = totalMatrix[index] + 1

    bestSplit = {
        'attribute': attributeName,
        'type' : 'numeric',
        'min' : None,
        'max': None,
        'entropy': sys.maxsize,
        'averageEntropy': None
    }

    chunks = []

    averageEntropy = 0

    for itemIndex in range(0, len(ranges[0])):
        countMatrix = [0] * len(unique)
        for element in list:
            if ranges[0][itemIndex] <= element[attributeName] <= ranges[1][itemIndex]:
                for index in range(0, len(unique)):
                    if element['class'] == Utils.getFromSetByIndex(unique, index):
                        countMatrix[index] = countMatrix[index] + 1

        entropy = 0
        total = sum(countMatrix)
        for index in range(0, len(unique)):
            p = (countMatrix[index] + .001) / (total + .001)
            entropy = entropy - p * math.log(p, len(unique))
        # print(f'{ranges[0][itemIndex]} {ranges[1][itemIndex]} {entropy}')

        averageEntropy = averageEntropy + entropy

        if entropy < bestSplit['entropy']:
            bestSplit['min'] = ranges[0][itemIndex]
            bestSplit['max'] = ranges[1][itemIndex]
            bestSplit['entropy'] = entropy

        chunk = {
            'attribute': attributeName,
            'type': 'numeric',
            'min': ranges[0][itemIndex],
            'max': ranges[1][itemIndex],
            'entropy': entropy
        }
        chunks.append(chunk)

    bestSplit['averageEntropy'] = averageEntropy/len(ranges[0])
    # print(f'{bestSplit}')
    return bestSplit, chunks

def getBestSplitCategorical(list, attributeName):
    list.sort(key=lambda k: k[attributeName])
    unique = Utils.retrieveSet(list, 'class')
    ranges = Utils.retrieveSet(list, attributeName)

    totalMatrix = [0] * len(unique)
    for item in list:
        for index in range(0, len(unique)):
            if item['class'] == Utils.getFromSetByIndex(unique, index):
                totalMatrix[index] = totalMatrix[index] + 1

    bestSplit = {
        'attribute' : attributeName,
        'type': 'categorical',
        'value' : None,
        'entropy': sys.maxsize,
        'averageEntropy': None
    }

    chunks = []

    averageEntropy = 0

    for item in ranges:
        countMatrix = [0] * len(unique)
        for element in list:
            if element[attributeName] == item:
                for index in range(0, len(unique)):
                    if element['class'] == Utils.getFromSetByIndex(unique, index):
                        countMatrix[index] = countMatrix[index] + 1

        entropy = 0
        total = sum(countMatrix)
        for index in range(0, len(unique)):
            p = (countMatrix[index] + .001)/(total + .001)
            entropy = entropy - p*math.log(p, len(unique))
        # print(f'{item} {entropy}')

        averageEntropy = averageEntropy + entropy

        if entropy < bestSplit['entropy']:
            bestSplit['value'] = item
            bestSplit['entropy'] = entropy

        chunk = {
            'attribute': attributeName,
            'type': 'categorical',
            'value': item,
            'entropy': entropy
        }
        chunks.append(chunk)

    bestSplit['averageEntropy'] = averageEntropy/len(ranges)
    # print(f'{bestSplit}')
    return bestSplit, chunks

def FFT(list, chunks):
    chunks.sort(key=lambda k: k['entropy'])
    chunk = chunks.pop(0)
    # chunk = chunks.pop(0)
    attributeName = chunk['attribute']

    unique = Utils.retrieveSet(list, 'class')
    total = 0

    classMatrix = ['']*len(unique)
    nodeStatistics = None

    classMatrixIndex = 0
    for item in unique:
        classMatrix[classMatrixIndex] = item
        classMatrixIndex = classMatrixIndex + 1

    countMatrix = [0]*len(unique)
    probabilityIndex = [0]*len(unique)

    newList = []
    if chunk['type'] == 'categorical':
        for item in list:
            if item[attributeName] == chunk['value'] :
                total = total + 1
                for index in range(0, len(unique)):
                    if item['class'] == Utils.getFromSetByIndex(unique, index):
                        countMatrix[index] = countMatrix[index] + 1
            else:
                newList.append(item)

        nodeStatistics = {
            'attribute': attributeName,
            'type': 'categorical',
            'value': chunk['value'],
            'class': classMatrix,
            'probability': None
        }

        for index in range(0, len(probabilityIndex)):
            probabilityIndex[index] = (countMatrix[index] + .001) / (total + .001)

        nodeStatistics['probability'] = probabilityIndex

    if chunk['type'] == 'numeric':
        for item in list:
            if chunk['min'] <= item[attributeName] <= chunk['max'] :
                total = total + 1
                for index in range(0, len(unique)):
                    if item['class'] == Utils.getFromSetByIndex(unique, index):
                        countMatrix[index] = countMatrix[index] + 1
            else:
                newList.append(item)

        nodeStatistics = {
            'attribute': attributeName,
            'type': 'numeric',
            'min': chunk['min'],
            'max': chunk['max'],
            'class': classMatrix,
            'probability': None
        }

        for index in range(0, len(probabilityIndex)):
            probabilityIndex[index] = (countMatrix[index] + .001) / (total + .001)

        nodeStatistics['probability'] = probabilityIndex

    # print(f'{len(newList)} {nodeStatistics}')
    return newList, chunks, nodeStatistics

