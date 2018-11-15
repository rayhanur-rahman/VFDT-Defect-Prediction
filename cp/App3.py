import csv, re, Utils, math, sys, Node, timeit, os, psutil

def readRowsLineByLine(csvFile, classIndex, split, root, locIndex):
    list = []
    numeric = []
    categorical = []
    chunks = []
    streamIndex = 0
    loc = 0
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

            if attributeIndex == locIndex: loc = loc + item
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




        if streamIndex%100 is 0:
            pass
            # print(f'{streamIndex} examples processed so far...')
            # process = psutil.Process(os.getpid())
            # memory = process.memory_info()[0] / float(2 ** 20)
            # print(memory)

        if streamIndex >= split :
            # print(f'loc read: {loc}')
            break

    return list, chunks, root, loc

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
        # if streamIndex > split:
        if True:
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

    return Utils.calCulateFMeasure(predictionMatrix)


def dump(trainFile, testFile, output, maxloc, maxSize, locIndex):
    print(trainFile)
    root = None
    start = None
    stop = None

    list = [.01, .02, .03, .04, .05, .06,
            .07, .08, .09, .1, .2, .3,
            .4, .5, .6, .7, .8, .9,
            1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
            80, 85, 90, 95, 100]
    # list = [.01]

    file = open(output, 'w')
    file.write('data-size, loc, accuracy, precision, recall, false-alarm, d2h, f1-score, ifa, training-time\n')

    for item in list:
        print(item)
        root = Node.Node('root')
        start = timeit.default_timer()
        split = (maxSize*item)/100
        result = readRowsLineByLine(trainFile, 0, split, root, locIndex)
        loc = result[3]
        stop = timeit.default_timer()
        root.deadEnd = False
        trainTime = stop - start
        result = readRowsForTest(testFile, 0, split, root)
        file.write(f'{item}, {100*loc/maxloc:.2f}, {100*result[0]:.2f}, {100*result[1]:.2f}, {100*result[2]:.2f}, {100*result[3]:.2f}, {100*result[4]:.2f}, {100*result[5]:.2f}, {result[6]}, {2000*trainTime/split:.2f}\n')
        root = None
    file.close()
    return

dump('abinit-train.csv', 'abinit-test.csv', 'abinit-dump-vfdt.csv', 7421221, 80789, 19)
dump('lammps-train.csv', 'lammps-test.csv', 'lammps-dump-vfdt.csv', 16755210, 37218, 19)
dump('libmesh-train.csv', 'libmesh-test.csv','libmesh-dump-vfdt.csv', 7301355, 22302, 19)
dump('mda-train.csv', 'mda-test.csv', 'mda-dump-vfdt.csv', 2011819, 10588, 14)