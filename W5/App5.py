import math, random, Num, Sym, Rows, csv, Model, sys, Dicretizer, prettytable



table = Rows.TableLoader("weatherLong.csv")
table.loadTableWithGenerator()


filteredData = []

for item in table.listOfDataAsDictionary:
    item['minRange'] = item['maxRange'] = item['corrupted'] = None
    item['dominationScore'] = 0
    for key in item:
        if item[key] == '?':
            item['corrupted'] = True
    if item['corrupted'] is None: filteredData.append(item)

random.seed(0)

for item in filteredData:
    a = item
    for i in range(0,100):
        b = filteredData[random.randint(0, len(filteredData) - 1)]
        s1 = 0
        s2 = 0
        for index in range(0, len(table.titles)):
            if index in table.minimizetionGoal:
                # print(a[table.titles[index]])
                # print(b[table.titles[index]])
                num = next((x for x in table.nums if x.title == table.titles[index]), None)
                x = num.getNormalizedValue(a[table.titles[index]])
                y = num.getNormalizedValue(b[table.titles[index]])
                # print(x)
                # print(y)
                s1 = s1 - math.pow(10, -1 * (x - y) / num.count)
                s2 = s2 - math.pow(10, -1 * (y - x) / num.count)
            if index in table.maximizationGoal:
                # print(a[table.titles[index]])
                # print(b[table.titles[index]])
                num = next((x for x in table.nums if x.title == table.titles[index]), None)
                x = num.getNormalizedValue(a[table.titles[index]])
                y = num.getNormalizedValue(b[table.titles[index]])
                # print(x)
                # print(y)
                s1 = s1 - math.pow(10, 1 * (x - y) / num.count)
                s2 = s2 - math.pow(10, 1 * (y - x) / num.count)
        if s1 < s2: item['dominationScore'] = item['dominationScore'] + 1/100

filteredData.sort(key=lambda k: k['dominationScore'], reverse=True)



pt = prettytable.PrettyTable()

list = []
for key in filteredData[0]:
    list.append(key)
pt.field_names = list



for index in range(0, 5):
    list = []
    for key in filteredData[index]:
        list.append(str(filteredData[index][key]))
    pt.add_row(list)

for index in range(len(filteredData) - 5, len(filteredData)):
    list = []
    for key in filteredData[index]:
        list.append(str(filteredData[index][key]))
    pt.add_row(list)



print(pt)