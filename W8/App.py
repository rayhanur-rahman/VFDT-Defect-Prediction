import sys, math, random, Num, Sym, Rows, Sample, Optimizer, SupervisedDiscretizer, Dicretizer, prettytable
print('warning: my output is a little bit verbose...')
print('only look for the best cut line if you are in a hurry\n')
print('FFT unsuper for auto')
optimizer1 = Optimizer.Dom()
result = optimizer1.getScore("auto.csv")
filteredData = result[0]
table = result[2]

def cut(filteredData, table):

    bestCut = {}
    bestCut['score'] = 0

    for x in table.independents:
        rowName = table.titles[x]
        filteredData.sort(key=lambda k: k[rowName])
        enough = math.pow(len(filteredData), 0.5)
        margin = 1.00
        queue = []
        queue.append(filteredData)
        discretizedData = []

        while len(queue) != 0:
            poppedItem = queue.pop(0)
            low = 0
            high = len(poppedItem)
            min = sys.maxsize
            max = -sys.maxsize
            if high - low <= 2 * math.ceil(enough):
                for element in poppedItem:
                    if min > element[rowName]:
                        min = element[rowName]
                    if max < element[rowName]:
                        max = element[rowName]
                for element in poppedItem:
                    element['maxRange'] = max
                    element['minRange'] = min
                for x in poppedItem:
                    if len(x) > 0:
                        discretizedData.append(x)
                continue
            num1 = Num.Num("", None)
            num2 = Num.Num("", None)
            for item in poppedItem:
                num1.increment(item[rowName])
            best = num1.sd
            cutIndex = None
            count = 0
            for item in poppedItem:
                num1.decrement(item[rowName])
                num2.increment(item[rowName])
                if num1.count >= math.ceil(enough) and num2.count >= math.ceil(enough):
                    expectedValueOfSd = num1.getExpectedValue(num2) * 1.05
                    if expectedValueOfSd < best * margin:
                        cutIndex = count
                        best = expectedValueOfSd
                count = count + 1
            if cutIndex is not None:
                list1 = []
                list2 = []
                for index in range(0, len(poppedItem)):
                    if index <= cutIndex:
                        list1.append(poppedItem[index])
                    else:
                        list2.append(poppedItem[index])

                if len(list1) > 0: queue.append(list1)
                if len(list2) > 0: queue.append(list2)

            if cutIndex is None:
                for element in poppedItem:
                    if min > element[rowName]:
                        min = element[rowName]
                    if max < element[rowName]:
                        max = element[rowName]
                for element in poppedItem:
                    element['maxRange'] = max
                    element['minRange'] = min
                for x in poppedItem:
                    if len(x) > 0:
                        discretizedData.append(x)

        discretizedData.sort(key=lambda k: k['minRange'], reverse=False)

        list = []
        for item in discretizedData:
            list.append(item['minRange'])

        print(f'{rowName}')
        unique = set(list)

        for element in unique:
            sum = 0
            count = 0
            for item in discretizedData:
                if item['minRange'] == element:
                    count = count + 1
                    sum = sum + item['dominationScore']
            maxRange = [x for x in discretizedData if x['minRange'] == element][0]['maxRange']
            print(f'{element} <= {rowName} <= {maxRange}: {sum/count:.2f}')
            if bestCut['score'] < sum / count:
                bestCut['type'] = 'numeric'
                bestCut['column'] = rowName
                bestCut['score'] = sum / count
                bestCut['start'] = element
                bestCut['end'] = maxRange
                bestCut['equals'] = None

        print("")
    for x in table.symbolicIndependents:
        filteredData.sort(key=lambda k: k[table.titles[x]])

        list = []
        for item in filteredData:
            list.append(item[table.titles[x]])

        unique = set(list)
        print(f'{table.titles[x]} = {unique}')
        for element in unique:
            sum3 = 0
            count = 0
            for item in filteredData:
                if item[table.titles[x]] == element:
                    count = count + 1
                    sum3 = sum3 + item['dominationScore']
            print(f'{table.titles[x]} = {element} : {sum3/count:.3f}')
            if bestCut['score'] < sum3 / count:
                bestCut['type'] = 'symbolic'
                bestCut['column'] = table.titles[x]
                bestCut['score'] = sum3 / count
                bestCut['start'] = None
                bestCut['end'] = None
                bestCut['equals'] = element
        print("")

    if bestCut['score'] == 0:
        return None
    print(f'best cut is {bestCut}')
    if bestCut['type'] == 'symbolic':
        new_list = [item for item in filteredData if item[bestCut['column']] != bestCut['equals']]
    else:
        new_list = [item for item in filteredData if
                    bestCut['start'] > item[bestCut['column']] or item[bestCut['column']] > bestCut['end']]

    return new_list

for i in range(1, 5):
    filteredData = cut(filteredData, table)
    print(f'end of pass {i}\n###############\n')
    if filteredData == None:
        print('end of iteration')
        break

print('FFT unuper for weatherLong')
optimizer2 = Optimizer.Dom()
result = optimizer2.getScore("weatherLong.csv")
filteredData = result[0]
table = result[2]
for i in range(1, 5):
    filteredData = cut(filteredData, table)
    print(f'end of pass {i}\n###############\n')
    if filteredData == None:
        print('end of iteration')
        break