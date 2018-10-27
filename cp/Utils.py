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

list = [64,64,72,72,81,81,83,83,69,69,65,65,75,75,75,75,68,68,85,85,80,80,71,71,72,72,70,70]

def getDiscretizedRange(data, attribute):
    list = []
    for item in data:
        list.append(item[attribute])
    cuts = []
    list.sort()
    enough = math.pow(len(list), 0.5)
    queue = []
    queue.append(list)
    discretizedData = []

    while len(queue) != 0:
        poppedItem = queue.pop(0)
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
            list1 = []
            list2 = []
            for index in range(0, len(poppedItem)):
                if index <= cutIndex:
                    list1.append(poppedItem[index])
                else:
                    list2.append(poppedItem[index])

            if len(list1) > 0: queue.append(list1)
            if len(list2) > 0: queue.append(list2)


    cuts.sort()
    return cuts

def getFromSetByIndex(set, index):
    count = 0
    for item in set:
        if count is index:
            return item
        count = count + 1
    return
