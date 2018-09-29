import Dicretizer
import Optimizer
import math, sys, Sym, Num, prettytable, Rows

optimizer1 = Optimizer.Dom()
filteredData = optimizer1.getScore("auto.csv")
rowName = '$model'
table = Rows.TableLoader("auto.csv")
table.loadTableWithGenerator()

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
    if high - low < 2 * math.ceil(enough):
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

    num3 = Num.Num("", None)
    num4 = Num.Num("", None)

    for item in poppedItem:
        num1.increment(item[rowName])
        num3.increment(item['dominationScore'])
    best = num1.sd
    best2 = num3.sd
    mean = num3.mean

    cutIndex = None
    count = 0
    for item in poppedItem:
        num1.decrement(item[rowName])
        num2.increment(item[rowName])
        num3.decrement(item['dominationScore'])
        num4.increment(item['dominationScore'])
        if num1.count >= math.ceil(enough) and num2.count >= math.ceil(enough):
            expectedValueOfSd = num1.getExpectedValue(num2) * 1.05
            expectedValueOfSd2 = num3.getExpectedValue(num4) * 1.05
            if expectedValueOfSd < best * margin:
                if expectedValueOfSd2 < best2 * margin:
                    cutIndex = count
                    best = expectedValueOfSd
                    best2 = expectedValueOfSd2
                    mean = num4.mean
        count = count + 1

    if cutIndex is not None:
        print(f'{poppedItem[0][rowName]} - {poppedItem[cutIndex -1][rowName]} - {poppedItem[-1][rowName]}--- {mean * 100: .0f}')
        list1 = []
        list2 = []
        for index in range(0, len(poppedItem)):
            if index < cutIndex:
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

discretizedData.sort(key=lambda k: k['minRange'])

pt = prettytable.PrettyTable()
list = []

for i in range(0, len(table.titles)):
    if i not in table.toBeIgnored:
        list.append(table.titles[i])

list.append((rowName + "-range"))
list.append('dominationScore')
pt.field_names = list
list = []

for item in discretizedData:
    for x in range(0, len(table.titles)):
        if x not in table.toBeIgnored:
            list.append(str(item[table.titles[x]]))
    list.append(str(item["minRange"]) + "-" + str(item["maxRange"]))
    list.append(str(item['dominationScore']))

    pt.add_row(list)
    list = []

print(pt)
