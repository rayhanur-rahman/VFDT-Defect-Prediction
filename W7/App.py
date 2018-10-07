import math, random, Num, Sym, Rows, Sample, Optimizer, SupervisedDiscretizer, Dicretizer, prettytable
print('warning: my output is a little bit verbose...')
print('only look for the best cut line if you are in a hurry\n')
print('FFT for auto')
optimizer1 = Optimizer.Dom()
result = optimizer1.getScore("auto.csv")
data = result[0]
table = result[2]

def cut(data, table):

    bestCut = {}
    bestCut['score'] = 0

    for x in table.independents:
        print(table.titles[x])
        data.sort(key=lambda k: k[table.titles[x]])

        min = data[0][table.titles[x]]
        med = data[math.floor(len(data) / 2)][table.titles[x]]
        max = data[-1][table.titles[x]]

        sum = 0
        avg = 0
        for index in range(0, math.floor(len(data) / 2)):
            sum = sum + data[index]['dominationScore']
        avg = sum / (len(data) / 2)

        sum2 = 0
        avg2 = 0
        for index in range(math.floor(len(data) / 2), len(data)):
            sum2 = sum2 + data[index]['dominationScore']
        avg2 = sum2 / (len(data) / 2)

        print(f'{min} <= {table.titles[x]} <= {med-1} : {avg:.3f}')
        print(f'{med} <= {table.titles[x]} <= {max} : {avg2:.3f}')
        if bestCut['score'] < avg or bestCut['score'] < avg2:
            if avg > avg2:
                bestCut['type'] = 'numeric'
                bestCut['column'] = table.titles[x]
                bestCut['score'] = avg
                bestCut['start'] = min
                bestCut['end'] = med - 1
                bestCut['equals'] = None
            else:
                bestCut['type'] = 'numeric'
                bestCut['column'] = table.titles[x]
                bestCut['score'] = avg2
                bestCut['start'] = med
                bestCut['end'] = max
                bestCut['equals'] = None

    for x in table.symbolicIndependents:
        data.sort(key=lambda k: k[table.titles[x]])

        list = []
        for item in data:
            list.append(item[table.titles[x]])

        unique = set(list)
        print(f'{table.titles[x]} = {unique}')
        for element in unique:
            sum3 = 0
            count = 0
            for item in data:
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
    print(f'best cut is: {bestCut}')
    if bestCut['type'] == 'symbolic':
        new_list = [item for item in data if item[bestCut['column']] != bestCut['equals']]
    else:
        new_list = [item for item in data if bestCut['start'] > item[bestCut['column']] or item[bestCut['column']] > bestCut['end']]
    return new_list


for i in range(1, 5):
    data = cut(data, table)
    print(f'end of pass {i}\n###############\n')
    if data == None:
        print('end of iteration')
        break

print("##################################################################\n")
print('FFT for weatherLong')
optimizer2 = Optimizer.Dom()
result = optimizer2.getScore("weatherLong.csv")
data = result[0]
table = result[2]

for i in range(1, 5):
    data = cut(data, table)
    print(f'end of pass {i}\n###############\n')
    if data == None:
        print('end of iteration')
        break