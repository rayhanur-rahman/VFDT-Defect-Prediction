import csv, re, Utils, math, sys, Node, timeit


def readRowsLineByLine(csvFile, classIndex, split, root):
    list = []
    numeric = []
    categorical = []
    chunks = []
    streamIndex = 0
    for row in Utils.csvRowsGenerator(csvFile):
        attributeIndex = 0
        dictionary = {}
        for item in row:
            isNumeric = None
            if Utils.getType(item.strip()) is "num":
                item = float(item.strip())
                isNumeric = True
            elif Utils.getType(item.strip()) is "str":
                item = str(item.strip())
                isNumeric = False
            else:
                return
            if attributeIndex == classIndex:
                dictionary['class'] = item
            else:
                key = 'a' + str(attributeIndex)
                dictionary[key] = item
                if streamIndex is 0:
                    if isNumeric:
                        numeric.append(key)
                    else:
                      categorical.append(key)

            attributeIndex = attributeIndex + 1
        list.append(dictionary)

        root.numeric = numeric
        root.categorical = categorical

        if root.deadEnd == False:
            Node.visitTree(root, dictionary, minDepth=3, pushExamplesToLeaf=False, isAdaptive=False)

        else:
            # print(f'finished building the tree with {streamIndex} examples')
            break

        streamIndex = streamIndex + 1




        if streamIndex%1000 is 0:
            pass
            # print(f'{streamIndex} examples processed so far...')

        if streamIndex >= split :
            # print('fuck')
            break

    return list, chunks, root

def readRowsForTest(csvFile, classIndex, split, root):
    list = []
    numeric = []
    categorical = []
    chunks = []
    streamIndex = 0
    hits = []
    miss = []
    predictionMatrix = []
    for row in Utils.csvRowsGenerator(csvFile):
        if streamIndex > split:
            attributeIndex = 0
            dictionary = {}
            for item in row:
                isNumeric = None
                if Utils.getType(item.strip()) is "num":
                    item = float(item.strip())
                    isNumeric = True
                elif Utils.getType(item.strip()) is "str":
                    item = str(item.strip())
                    isNumeric = False
                else:
                    return
                if attributeIndex == classIndex:
                    dictionary['class'] = item
                else:
                    key = 'a' + str(attributeIndex)
                    dictionary[key] = item
                    if streamIndex is 0:
                        if isNumeric:
                            numeric.append(key)
                        else:
                          categorical.append(key)

                attributeIndex = attributeIndex + 1
            list.append(dictionary)

            root.numeric = numeric
            root.categorical = categorical

            Node.visiTreeForTest(root, dictionary, hits, miss, predictionMatrix)

        streamIndex = streamIndex + 1

        if streamIndex%100000 is 0:
            pass
            # print(f'{streamIndex} examples processed so far...')

    # print(f'finished building the tree with {len(hits)+len(miss)} examples')
    # print(f'{len(hits)} # {len(miss)}')

    Utils.calCulateFMeasure(predictionMatrix)

    return


root = None
start = None
stop = None

for i in range(9991, 10000, 1):
    print(f'{i/100}%:')
    root = Node.Node('root')
    start = timeit.default_timer()
    split = 89303*((100-(i/100))/100)
    result = readRowsLineByLine("bugs-test.csv", 0, split, root)
    stop = timeit.default_timer()
    root.deadEnd = False
    print(f'training time: {stop - start}')
    start = timeit.default_timer()
    readRowsForTest('bugs-test.csv', 0, split, root)
    stop = timeit.default_timer()
    print(f'testing time: {stop - start}')
    root = None

