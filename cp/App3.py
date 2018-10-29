import csv, re, Utils, math, sys, Node

root = Node.Node('root')

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
                    if isNumeric:
                        numeric.append(key)
                    else:
                      categorical.append(key)

            attributeIndex = attributeIndex + 1
        list.append(dictionary)

        root.numeric = numeric
        root.categorical = categorical

        if root.deadEnd == False:
            Node.visitTree(root, dictionary)

        else:
            print(f'finished building the tree with {streamIndex} exaples')
            break

        streamIndex = streamIndex + 1

        if streamIndex%10000 is 0:
            pass
            print(f'{streamIndex} examples processed so far...')
            # Node.preOrder(root)
            # print(f'#############################\n')

    return list, chunks, root

result = readRowsLineByLine("/media/rr/8E30E13030E12047/bigdata/higgs.csv", classIndex=0)
# result = readRowsLineByLine("iris.csv", classIndex=4)
# result = readRowsLineByLine("weatherLong.csv", classIndex=4)
# result = readRowsLineByLine("d.csv", classIndex=0)
# result = readRowsLineByLine("data.csv", classIndex=0)


x = Node.preOrder(root)

