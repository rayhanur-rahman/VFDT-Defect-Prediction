import csv, re, Utils, math, sys, Node, timeit

root = Node.Node('root')

numericIndex = []
categoricalIndex = []

for i in range (1,11):
    numericIndex.append('a' + str(i))

for i in range (11,55):
    categoricalIndex.append('a' + str(i))


def readRowsLineByLine(csvFile, classIndex):
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
                    pass
                    # if isNumeric:
                    #     numeric.append(key)
                    # else:
                    #   categorical.append(key)

            if streamIndex is 0:
                numeric = numericIndex
                categorical = categoricalIndex

            attributeIndex = attributeIndex + 1
        list.append(dictionary)

        root.numeric = numeric
        root.categorical = categorical

        if root.deadEnd == False:
            Node.visitTree(root, dictionary, minDepth=3, pushExamplesToLeaf=False, isAdaptive=False)

        else:
            print(f'finished building the tree with {streamIndex} examples')
            break

        streamIndex = streamIndex + 1

        if streamIndex%100 is 0:
            print(f'{streamIndex} examples processed so far...')

    return list, chunks, root

start = timeit.default_timer()

# result = readRowsLineByLine("/media/rr/8E30E13030E12047/bigdata/higgs.csv", classIndex=0)
# result = readRowsLineByLine("iris.csv", classIndex=4)
# result = readRowsLineByLine("weatherLong.csv", classIndex=4)
# result = readRowsLineByLine("d.csv", classIndex=0)
# result = readRowsLineByLine("data.csv", classIndex=0)
# result = readRowsLineByLine("bugs.csv", classIndex=0)
result = readRowsLineByLine("forest.csv", classIndex=0)

# x = Node.preOrder(root)




def readRowsForTest(csvFile, classIndex):
    list = []
    numeric = []
    categorical = []
    chunks = []
    streamIndex = 0
    hits = []
    miss = []
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


        Node.visiTreeForTest(root, dictionary, hits, miss)

        streamIndex = streamIndex + 1

        if streamIndex%10000 is 0:
            pass
            print(f'{streamIndex} examples processed so far...')

    print(f'finished building the tree with {streamIndex} examples')
    print(f'{len(hits)} # {len(miss)}')

    return

root.deadEnd = False
# readRowsForTest('test.csv', 0)
# readRowsForTest('test4.csv', 0)
readRowsForTest('test5.csv', 0)

stop = timeit.default_timer()

print(f'execution time: {stop - start}')