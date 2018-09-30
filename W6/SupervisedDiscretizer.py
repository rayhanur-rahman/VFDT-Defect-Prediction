import Dicretizer
import Optimizer
import math, sys, Sym, Num, prettytable, Rows, Node

class SupervisedDiscretizer:
    def __init__(self, csvFile):
        self.csvFile = csvFile
        self.filteredData = None
        self.table = None
        self.preProcess()

    def preProcess(self):
        optimizer1 = Optimizer.Dom()
        self.filteredData = optimizer1.getScore(self.csvFile)[0]
        self.table = Rows.TableLoader(self.csvFile)
        self.table.loadTableWithGenerator()

    def discretize(self, rowName):
        self.filteredData.sort(key=lambda k: k[rowName])
        enough = math.pow(len(self.filteredData), 0.5)
        margin = 1.00
        queue = []
        queue.append(self.filteredData)
        discretizedData = []

        tree = []
        node = Node.Node(self.filteredData[0][rowName], self.filteredData[-1][rowName], 0, 0, 0, len(self.filteredData))
        tree.append(node)

        while len(queue) != 0:
            poppedItem = queue.pop(0)
            low = 0
            high = len(poppedItem)
            min = sys.maxsize
            max = -sys.maxsize
            if high - low <= 2 * math.ceil(enough):
                sum = 0
                for item in poppedItem:
                    sum = sum + item['dominationScore']
                # print(f'LEAF -> {poppedItem[0][rowName]} - {poppedItem[-1][rowName]} --- {(sum/len(poppedItem)) * 100: .0f}')
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

            mean1 = num3.mean
            mean2 = num4.mean
            var1 = num3.variance
            var2 = num4.variance
            sd1 = num3.sd
            sd2 = num4.sd
            count1 = num3.count
            count2 = num4.count

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
                            mean1 = num3.mean
                            mean2 = num4.mean
                            var1 = num3.variance
                            var2 = num4.variance
                            sd1 = num3.sd
                            sd2 = num4.sd
                            count1 = num3.count
                            count2 = num4.count
                count = count + 1

            if cutIndex is not None:
                # print(f'NODE -> {poppedItem[0][rowName]} - {poppedItem[-1][rowName]}')
                list1 = []
                list2 = []
                for index in range(0, len(poppedItem)):
                    if index <= cutIndex:
                        list1.append(poppedItem[index])
                    else:
                        list2.append(poppedItem[index])

                node1 = Node.Node(poppedItem[0][rowName], poppedItem[cutIndex][rowName], mean1, var1, sd1, count1)
                node2 = Node.Node(poppedItem[cutIndex + 1][rowName], poppedItem[len(poppedItem) - 1][rowName], mean2,
                                  var2, sd2, count2)

                # print(f'@@@{node1.min} {node1.max} {node2.min} {node2.max}')
                # for x in tree:
                #     print(f'### {x.min} {x.max}')

                node = next((x for x in tree if x.min == node1.min and x.max == node2.max), None)
                node.children.append(node1)
                node.children.append(node2)
                tree.append(node1)
                tree.append(node2)

                if len(list1) > 0: queue.append(list1)
                if len(list2) > 0: queue.append(list2)

            if cutIndex is None:
                # print(f'LEAF -> {poppedItem[0][rowName]} - {poppedItem[-1][rowName]} --- {mean * 100: .0f}')
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

        for i in range(0, len(self.table.titles)):
            if i not in self.table.toBeIgnored:
                list.append(self.table.titles[i])

        list.append((rowName + "-range"))
        list.append('dominationScore')
        pt.field_names = list
        list = []

        for item in discretizedData:
            for x in range(0, len(self.table.titles)):
                if x not in self.table.toBeIgnored:
                    list.append(str(item[self.table.titles[x]]))
            list.append(str(item["minRange"]) + "-" + str(item["maxRange"]))
            list.append(str(item['dominationScore']))

            pt.add_row(list)
            list = []

        # print(pt)

        node = tree[0]
        leaf = []

        print(f'discretization performed on {rowName}')
        def visit(node, depth):
            depth = depth
            for i in range(0, depth):
                print("|--", end="")
            if len(node.children) > 0:
                print(f'{node.min: .0f}..{node.max:.0f}')
                depth = depth + 1
            else:
                leaf.append(node)
                print(f'{node.min: .0f}..{node.max:.0f} : mean = {node.mean*100: .0f} and size = {node.count:.0f}')
            for child in node.children:
                visit(child, depth)

        visit(node, 0)

        sumOfSplitSize = 0

        for x in leaf:
            sumOfSplitSize = sumOfSplitSize + x.count

        splitValue = 0
        for x in leaf:
            splitValue = splitValue + (x.count*x.sd)/sumOfSplitSize

        print(f'std dev of all splits on {rowName} = {splitValue}')
        print('---###---\n')
        return [rowName, discretizedData, pt, splitValue]

    def discretizeAll(self):
        tuples = []
        for x in range(0, len(self.table.titles)):
            if x in self.table.independents:
                tuples.append(self.discretize(self.table.titles[x]))


        pt = prettytable.PrettyTable()
        pt.field_names = ['attribute', 'split value']

        for t in tuples:
            pt.add_row([t[0], t[3]])

        print(pt)

        for t in tuples:
            print(t[2])