import csv, re, Utils, math, sys, timeit

def readRowsLineByLine(csvFile, split, classIndex):
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
        streamIndex = streamIndex + 1

        if streamIndex >= split :
            break

    splits = []
    chunks = []


    for item in numeric:
        out = Utils.getBestSplitNumericMedian(list, item)
        splits.append(out[0])
        for item in out[1]:
            chunks.append(item)


    for item in categorical:
        out = Utils.getBestSplitCategorical(list, item)
        splits.append(out[0])
        for item in out[1]:
            chunks.append(item)


    return list, chunks


# result = readRowsLineByLine("/home/rr/Workspace/NCSUFSS18/cp/lammps-train.csv", 2500, classIndex=0)

def formFFT(result):
    list = result[0]
    chunks = result[1]

    tree = []

    while True:
        out = Utils.FFT(list, chunks)
        if len(chunks) == 0 or len(out[0]) == len(list):
            unique = Utils.retrieveSet(list, 'class')
            totalMatrix = [0] * len(unique)
            classMatrix = [''] * len(unique)

            classMatrixIndex = 0
            for item in unique:
                classMatrix[classMatrixIndex] = item
                classMatrixIndex = classMatrixIndex + 1

            for item in list:
                for index in range(0, len(unique)):
                    if item['class'] == Utils.getFromSetByIndex(unique, index):
                        totalMatrix[index] = totalMatrix[index] + 1

            total = sum(totalMatrix)
            probabilityIndex = [0] * len(unique)
            for index in range(0, len(probabilityIndex)):
                probabilityIndex[index] = (totalMatrix[index] + .001) / (total + .001)

            tree.append({
                'type': 'leaf',
                'class': classMatrix,
                'probability': probabilityIndex
            })
            break
        list = out[0]
        chunks = out[1]
        tree.append(out[2])
        if len(tree) > 3:
            unique = Utils.retrieveSet(list, 'class')
            totalMatrix = [0] * len(unique)
            classMatrix = [''] * len(unique)

            classMatrixIndex = 0
            for item in unique:
                classMatrix[classMatrixIndex] = item
                classMatrixIndex = classMatrixIndex + 1

            for item in list:
                for index in range(0, len(unique)):
                    if item['class'] == Utils.getFromSetByIndex(unique, index):
                        totalMatrix[index] = totalMatrix[index] + 1

            total = sum(totalMatrix)
            probabilityIndex = [0] * len(unique)
            for index in range(0, len(probabilityIndex)):
                probabilityIndex[index] = (totalMatrix[index] + .001) / (total + .001)

            tree.append({
                'type': 'leaf',
                'class': classMatrix,
                'probability': probabilityIndex
            })
            break
    return tree

def readTestData(csvFile, classIndex):
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
        streamIndex = streamIndex + 1
    return list

# tree = formFFT(result)

# testList = readTestData('/home/rr/Workspace/NCSUFSS18/cp/lammps-test.csv', 0)

def predict(testData, tree):
    hits = 0
    miss = 0
    unpredicted = 0
    total = 0
    predictionMatrix = []
    for element in testData:
        predictedClass = None
        for item in tree:
            if item['type'] == 'numeric':
                x = element[item['attribute']]
                if item['min'] <= element[item['attribute']] <= item['max']:
                    maxProbability = -1
                    maxProbabilityIndex = 0
                    for p in item['probability']:
                        if p > maxProbability:
                            maxProbability = p
                            predictedClass = item['class'][maxProbabilityIndex]
                        maxProbabilityIndex = maxProbabilityIndex + 1

            if item['type'] == 'categorical':
                x = element[item['attribute']]
                if item['value'] == element[item['attribute']]:
                    maxProbability = -1
                    maxProbabilityIndex = 0
                    for p in item['probability']:
                        if p > maxProbability:
                            maxProbability = p
                            predictedClass = item['class'][maxProbabilityIndex]
                        maxProbabilityIndex = maxProbabilityIndex + 1

            if predictedClass != None and predictedClass == element['class']:
                # print(f'{predictedClass} {element["class"]} hit')
                hits = hits + 1
                predictionMatrix.append((element['class'], predictedClass, True))
                break

            if predictedClass != None and predictedClass != element['class']:
                # print(f'{predictedClass} {element["class"]} miss')
                miss = miss + 1
                predictionMatrix.append((element['class'], predictedClass, False))
                break

        if predictedClass == None:
            unpredicted = unpredicted + 1
            maxProbability = -1
            maxProbabilityIndex = 0
            for p in tree[-1]['probability']:
                if p > maxProbability:
                    maxProbability = p
                    predictedClass = tree[-1]['class'][maxProbabilityIndex]
                maxProbabilityIndex = maxProbabilityIndex + 1


            if predictedClass != None and predictedClass == element['class']:
                # print(f'{predictedClass} {element["class"]} hit')
                hits = hits + 1
                predictionMatrix.append((element['class'], predictedClass, True))
                continue


            if predictedClass != None and predictedClass != element['class']:
                # print(f'{predictedClass} {element["class"]} miss')
                miss = miss + 1
                predictionMatrix.append((element['class'], predictedClass, False))
                continue

        # pass


        total = total + 1

    return Utils.calCulateFMeasure(predictionMatrix)

# predict(testList, tree)


def dump(trainFile, testFile, output, maxSize):
    print(trainFile)
    start = None
    stop = None

    list = [.01, .02, .03, .04, .05, .06,
            .07, .08, .09, .1, .2, .3,
            .4, .5, .6, .7, .8, .9,
            1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
            80, 85, 90, 95, 100]
    # list = [.01]

    file = open(output, 'w')
    file.write('size, accuracy, precision, recall, fa, d2h, f1, time\n')

    for item in list:
        print(item)
        start = timeit.default_timer()
        split = (maxSize*item)/100
        result = readRowsLineByLine(trainFile, split, 0)
        tree = formFFT(result)
        stop = timeit.default_timer()
        trainTime = stop - start
        result = readTestData(testFile, 0)
        result = predict(result, tree)
        file.write(f'{item}, {100*result[0]:.2f}, {100*result[1]:.2f}, {100*result[2]:.2f}, {100*result[3]:.2f}, {100*result[4]:.2f}, {100*result[5]:.2f}, {1000*trainTime:.2f}\n')
    file.close()
    return


for x in range(1,11):
    datasets = ['abinit', 'lammps', 'libmesh', 'mda']
    size = [73096, 33677, 20185, 9607]
    path = '/home/rr/Workspace/NCSUFSS18/cp/datasets/'
    i = 0
    for set in datasets:
        dump(f'{path}{set}-train-{x}.csv', f'{path}{set}-test-{x}.csv', f'{set}-dump-fft-{x}.csv',size[i])
        i += 1


# dump('abinit-train.csv', 'abinit-test.csv', 'abinit-dump-fft.csv', 80789)
# dump('lammps-train.csv', 'lammps-test.csv', 'lammps-dump-fft.csv', 37218)
# dump('libmesh-train.csv', 'libmesh-test.csv','libmesh-dump-fft.csv', 22302)
# dump('mda-train.csv', 'mda-test.csv', 'mda-dump-fft.csv', 10588)


# i=0
# for x in range(1,101):
#     print(x)
#     datasets = ['abinit']
#     path = '/home/rr/Workspace/NCSUFSS18/cp/datasets/'
#     trainFile = path+'abinit-train-1.csv'
#     maxSize = 73096
#     start = timeit.default_timer()
#     split = (maxSize * x) / 100
#     result = readRowsLineByLine(trainFile, split, 0)
#     tree = formFFT(result)
#     stop = timeit.default_timer()
#     trainTime = stop - start
#
#     i = i + (stop-start)
# print(i)