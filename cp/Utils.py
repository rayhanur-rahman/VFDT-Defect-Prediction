import csv, re, Utils, Num, Sym, math, sys, timeit, numpy


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
    length = len(data)
    if length == 0: return None, None, None
    list = []
    for item in data:
        list.append(item[attribute])
    cuts = []
    list.sort()
    enough = math.pow(len(list), 0.5)
    queue = []
    queue.append(list)

    while len(queue) != 0:
        poppedItem = queue.pop(0)
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
            list1 = []
            list2 = []
            for index in range(0, len(poppedItem)):
                if index <= cutIndex:
                    list1.append(poppedItem[index])
                else:
                    list2.append(poppedItem[index])

            if len(list1) > 0:
                queue.append(list1)
            if len(list2) > 0:
                queue.append(list2)


    cuts.sort()
    minRange = []
    maxRange = []
    cutIndex = 0
    listIndex  = 0
    minIndex = 0

    if len(cuts) > 0:
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
    else:
        minRange.append(list[0])
        maxRange.append(list[-1])
    # print(f'{cuts} {minRange} {maxRange}')
    return minRange, maxRange, cuts


def getDiscretizedRangeNumPy(data, attribute):
    length = len(data)
    if length == 0: return None, None, None
    list = []
    for item in data:
        list.append(item[attribute])
    enough = math.pow(len(list), 0.5)
    # hist, bin_edges = numpy.histogram(list, bins=int( math.floor(enough) ))
    hist, bin_edges = numpy.histogram(list, bins=int( 3 ))


    minRange = []
    maxRange = []
    cuts = []

    for index in range(0, len(bin_edges)):
        cuts.append(int(bin_edges[index]))
        if index != len(bin_edges) - 1: minRange.append(int(bin_edges[index]))
        if index != 0: maxRange.append(int(bin_edges[index]))

    cuts = cuts[1:-1]
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

    rangeDictionary = {
        'min': ranges[0],
        'max': ranges[1]
    }

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
            if p == 1 and len(unique) == 1: entropy = entropy - 0
            else: entropy = entropy - p * math.log(p, len(unique))

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

        averageEntropy = averageEntropy + entropy*(total/len(list))

        chunks.append(chunk)

    bestSplit['averageEntropy'] = averageEntropy
    # print(f'{bestSplit}')
    return bestSplit, chunks, rangeDictionary

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
            if p == 1 and len(unique) == 1: entropy = entropy - 0
            else: entropy = entropy - p * math.log(p, len(unique))

        if entropy < bestSplit['entropy']:
            bestSplit['value'] = item
            bestSplit['entropy'] = entropy

        chunk = {
            'attribute': attributeName,
            'type': 'categorical',
            'value': item,
            'entropy': entropy
        }

        averageEntropy = averageEntropy + entropy * (total / len(list))
        chunks.append(chunk)

    bestSplit['averageEntropy'] = averageEntropy
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

def calCulateFMeasure(predictioMatrix):
    classes = []
    predictedClasses = []
    outcome = []
    for item in predictioMatrix:
        classes.append(item[0])
        predictedClasses.append(item[1])
        outcome.append(item[2])

    uniqueClasses = set(classes)

    TP = [0] * len(uniqueClasses)
    TN = [0] * len(uniqueClasses)
    FP = [0] * len(uniqueClasses)
    FN = [0] * len(uniqueClasses)

    # for 1
    ifa = 0
    ifaScoreCounted = False
    for uniqueClassIndex in range(0, len(uniqueClasses)):
        for index in range(0, len(predictedClasses)):
            if classes[index] == getFromSetByIndex(uniqueClasses, uniqueClassIndex) and \
                    predictedClasses[index] == getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and outcome[index] == True:
                TP[uniqueClassIndex] += 1
                if TP[uniqueClassIndex] == 1 and ifaScoreCounted == False:
                    ifa = FP[uniqueClassIndex]
                    ifaScoreCounted = True
            if classes[index] != getFromSetByIndex(uniqueClasses, uniqueClassIndex) and \
                    predictedClasses[index] != getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and outcome[index] == True:
                TN[uniqueClassIndex] += 1
            if classes[index] != getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and predictedClasses[index] == getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and outcome[index] == False:
                FP[uniqueClassIndex] += 1
            if classes[index] == getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and predictedClasses[index] != getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and outcome[index] == False:
                FN[uniqueClassIndex] += 1

    # print(f'{uniqueClasses}')
    # print(f'{ TP[0] / (TP[0] + FP[0] + .001) }')
    # print(f'{ TP[0] / (TP[0] + FN[0] + .001) }')
    # print(f'{ TP[1] / (TP[1] + FP[1] + .001) }')
    # print(f'{ TP[1] / (TP[1] + FN[1] + .001) }')

    accuracy = (TP[1] + FN[1])/(TP[1] + FP[1] + TN[1] + FN[1])

    precision = TP[1] / (TP[1] + FP[1] + .001)
    recall = TP[1] / (TP[1] + FN[1] + .001)
    falseAlarm = FP[1]/(FP[1]+FN[1] + .001)
    d2h = math.sqrt( (1-recall)*(1-recall) + falseAlarm*falseAlarm )
    f1score = (2*precision*recall)/(precision+recall+.001)
    # print(f'accuracy \t precison \t recall \t false alarm \t d2h \t f1 score')
    # print(f'{accuracy*100:.2f} {precision*100:.2f} {recall*100:.2f} {falseAlarm*100:.2f} {d2h*100:.2f} {f1score*100:.2f} {ifa}')
    return [accuracy, precision, recall, falseAlarm, d2h, f1score, ifa]