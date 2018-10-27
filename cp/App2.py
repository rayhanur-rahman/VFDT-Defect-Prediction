import csv, re, Utils, math, sys

list = []
numeric = []
categorical = []


def readRowsLineByLine(csvFile, classIndex):
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

        if streamIndex%100 is 0:
            pass




# readRowsLineByLine("/media/rr/8E30E13030E12047/bigdata/higgs.csv")
readRowsLineByLine("weatherLong.csv", classIndex=4)

list.sort(key=lambda k: k['a1'])
unique = Utils.retrieveSet(list, 'class')
ranges = Utils.getDiscretizedRange(list, 'a1')

totalMatrix = [0] * len(unique)
for item in list:
    for index in range(0, len(unique)):
        if item['class'] == Utils.getFromSetByIndex(unique, index):
            totalMatrix[index] = totalMatrix[index] + 1

bestSplit = [None, sys.maxsize]

for item in ranges:
    lowMatrix = [0] * len(unique)
    highMatrix = [0] * len(unique)
    for element in list:
        if element['a1'] <= item:
            for index in range(0, len(unique)):
                if element['class'] == Utils.getFromSetByIndex(unique, index):
                    lowMatrix[index] = lowMatrix[index] + 1
        else:
            for index in range(0, len(unique)):
                if element['class'] == Utils.getFromSetByIndex(unique, index):
                    highMatrix[index] = highMatrix[index] + 1


    entropy = 0
    for index in range(0, len(unique)):
        entropy = entropy + ( - (lowMatrix[index]/totalMatrix[index])*math.log((lowMatrix[index]/totalMatrix[index]), len(unique)) - (highMatrix[index]/totalMatrix[index])*math.log((highMatrix[index]/totalMatrix[index]), len(unique)) )

    if entropy < bestSplit[1]:
        bestSplit[0] = item
        bestSplit[1] = entropy

print(f'{bestSplit}')


# for element in unique2:





# print(numeric)
# print(categorical)



