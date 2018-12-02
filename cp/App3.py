import csv, re, Utils, math, sys, Node, timeit, os, psutil
from pympler import asizeof

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
            Node.visitTree(root, dictionary,
                           minDepth=3,
                           pushExamplesToLeaf=False,
                           isAdaptive=False,
                           nmin=1,
                           tie=.1,
                           split=50)

        else:
            # print(f'finished building the tree with {streamIndex} examples')
            break

        streamIndex = streamIndex + 1

        if streamIndex%100 is 0:
            print(streamIndex)
            pass
        # if streamIndex >= split :
        #     print(f'loc read: {loc}')
        #     break

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

    # list = [.01, .02, .03, .04, .05, .06,
    #         .07, .08, .09, .1, .2, .3,
    #         .4, .5, .6, .7, .8, .9,
    #         1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
    #         80, 85, 90, 95, 100]
    list = [100]

    file = open(output, 'w')
    file.write('size, accuracy, precision, recall, fa, d2h, f1, time\n')

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
        print(trainTime)
        result = readRowsForTest(testFile, 0, split, root)
        file.write(f'{item}, {100*result[0]:.2f}, {100*result[1]:.2f}, {100*result[2]:.2f}, {100*result[3]:.2f}, {100*result[4]:.2f}, {100*result[5]:.2f}, {1000*trainTime:.2f}\n')
        root = None
    file.close()
    return

# for x in range(1,2):m
#     datasets = ['abinit', 'lammps', 'libmesh', 'mda']
#     size = [73096, 33677, 20185, 9607]
#     datasets = ['abinit']
#     size = [73096]
#     path = '/home/rr/Workspace/NCSUFSS18/cp/datasets/'
#     i = 0
#     for set in datasets:
#         print(f'{set} {x}')
#         dump(f'{path}{set}-train-{x}.csv', f'{path}{set}-test-{x}.csv', f'{set}-dump-vfdt-{x}.csv', 100, size[i], 14)
#         i += 1

    # dump(f'/home/rr/Workspace/NCSUFSS18/cp/datasets/abinit-train.csv', f'abinit-test.csv', f'abinit-dump-vfdt.csv', 6728971, 73096, 19)
    # dump(f'lammps-train.csv', f'lammps-test.csv', f'lammps-dump-vfdt.csv', 15173205, 33677, 19)
    # dump(f'libmesh-train.csv', f'libmesh-test.csv',f'libmesh-dump-vfdt.csv', 6565557, 20185, 19)

dump(f'/run/media/rr/8E30E13030E12047/bigdata/higgs.csv', f'/run/media/rr/8E30E13030E12047/bigdata/higgs-test.csv', f'higgs-vfdt.csv', 1808907, 9607, 14)

