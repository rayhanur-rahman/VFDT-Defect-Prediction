import math, random, Num, Sym, Rows, csv, Model, sys, prettytable

class Unsupervised:
    def discretize(self, csvFile, rowName):
        table = Rows.TableLoader(csvFile)
        table.loadTableWithGenerator()
        filteredData = []

        for item in table.listOfDataAsDictionary:
            item['minRange'] = item['maxRange'] = item['corrupted'] = None
            if item[rowName] == '?':
                item['corrupted'] = True
            else:
                filteredData.append(item)

        table.listOfDataAsDictionary = None

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
            for item in poppedItem:
                num1.increment(item[rowName])
            best = num1.sd
            cut = None
            for item in poppedItem:
                num1.decrement(item[rowName])
                num2.increment(item[rowName])
                if num1.count >= enough and num2.count >= enough:
                    expectedValueOfSd = num1.getExpectedValue(num2) * 1.05
                    if expectedValueOfSd < best*margin:
                        cut = item[rowName]
            list1 = []
            list2 = []
            for item in poppedItem:
                if item[rowName] < cut:
                    list1.append(item)
                else:
                    list2.append(item)

            if len(list1) > 0: queue.append(list1)
            if len(list2) > 0: queue.append(list2)

        discretizedData.sort(key=lambda k: k['minRange'])

        pt = prettytable.PrettyTable()
        list = []

        for i in range(0, len(table.titles)):
            if i not in table.toBeIgnored:
                list.append(table.titles[i])

        list.append((rowName+"-range"))
        pt.field_names = list
        list  = []

        for item in discretizedData:
            for x in range(0, len(table.titles)):
                if x not in table.toBeIgnored:
                    list.append(str(item[table.titles[x]]))
            list.append(str(item["minRange"]) + "-" + str(item["maxRange"]))

            pt.add_row(list)
            list=[]


        print(pt)
        return discretizedData