import math, random, sys, Num, Sym, Utils

class Node:

    def __init__(self, name):
        self.name = name
        self.attribute = {
            'name': None,
            'type': None
        }
        self.split = None #information of the best split so far
        self.parent = None
        self.children = [] #list of Nodes
        self.examples = []
        self.ignoredAttribute = []
        self.classIndex = None
        self.probabilityIndex = None
        self.deadEnd = False
        self.numeric = []
        self.categorical = []
        return

def preOrder(node):
    if len(node.children) == 0:
        print(f'{len(node.examples)} # {node.classIndex} # {node.probabilityIndex} # {node.name}')
        # print(f'{node.name} {node.attribute} {node.split} {node.ignoredAttribute}')
        # print(f'{node.name} # {node.attribute} # {node.split} # {node.ignoredAttribute}')
        # print(f'{len(node.examples)} {node.classIndex} {node.probabilityIndex}')
    if len(node.children) > 0:
        for child in node.children:
            preOrder(child)
    return

def visitTree(node, example):

    if len(node.children) == 0:
        node.examples.append(example)

        # build statistics
        unique = Utils.retrieveSet(node.examples, 'class')
        classMatrix = [''] * len(unique)
        probabilityIndex = [0] * len(unique)
        classMatrixIndex = 0
        for item in unique:
            classMatrix[classMatrixIndex] = item
            classMatrixIndex = classMatrixIndex + 1
        totalMatrix = [0] * len(unique)
        for item in node.examples:
            for index in range(0, len(unique)):
                if item['class'] == Utils.getFromSetByIndex(unique, index):
                    totalMatrix[index] = totalMatrix[index] + 1
        total = sum(totalMatrix)
        for index in range(0, len(probabilityIndex)):
            probabilityIndex[index] = (totalMatrix[index] + .001) / (total + .001)
        node.classIndex = classMatrix
        node.probabilityIndex = probabilityIndex


        # check for epsilon
        splits = []
        chunks = []

        # print(f'1 {node.ignoredAttribute}')
        # print(f'2 {node.numeric}')
        # print(f'3 {categorical}')
        #
        for attr in node.ignoredAttribute:
            if attr['type'] == 'categorical':
                if attr['name'] in node.categorical: node.categorical.remove(attr['name'])
            if attr['type'] == 'numeric':
                if attr['name'] in node.numeric: node.numeric.remove(attr['name'])

        # print(f'4 {node.numeric}')
        # print(f'5 {categorical}')
        # print('###\n')

        for item in node.numeric:
            out = Utils.getBestSplitNumeric(node.examples, item)
            splits.append(out[0])
            for item in out[1]:
                chunks.append(item)

        for item in node.categorical:
            out = Utils.getBestSplitCategorical(node.examples, item)
            splits.append(out[0])
            for item in out[1]:
                chunks.append(item)

        splits.sort(key=lambda k: k['averageEntropy'])

        numberOfTotalAttributes = len(node.ignoredAttribute) + len(node.categorical) + len(node.numeric)

        # if len(node.ignoredAttribute) >= math.sqrt((numberOfTotalAttributes)):
        if len(node.ignoredAttribute) >= 3:
            if len(node.examples) > 49:
                node.deadEnd = True
            criticalPoint = 0

        elif len(splits) > 1:
            min = splits[0]['averageEntropy']
            max = splits[1]['averageEntropy']
            criticalPoint = (max - min)

        elif len(splits) <= 1:
            criticalPoint = 0
            node.deadEnd = True



        delta = .05
        unique = Utils.retrieveSet(node.examples, 'class')
        epsilon = math.log(len(unique), math.e) * math.sqrt((math.log(1 / delta, math.e)) / len(node.examples))
        # print(f'distance: {epsilon - criticalPoint}, total inputs: {len(node.examples)}')

        if epsilon - criticalPoint < 0:
            bestAttribute = splits[0]
            node.attribute['name'] = bestAttribute['attribute']
            node.attribute['type'] = bestAttribute['type']
            node.ignoredAttribute.append(node.attribute)
            # ranges = None
            if bestAttribute['type'] == 'numeric':
                ranges = Utils.getDiscretizedRange(node.examples, bestAttribute['attribute'])
                for index in range(0, len(ranges[0])):
                    child = Node('')
                    child.parent = node
                    child.split = {
                        'attribute': node.attribute['name'],
                        'type': 'numeric',
                        'min': ranges[0][index],
                        'max': ranges[1][index]
                    }
                    child.name = child.parent.name + ' .. ' + str(child.split['min']) + ' <= ' + child.split['attribute'] + ' <= ' + str(child.split['max'])
                    for attr in node.ignoredAttribute:
                        child.ignoredAttribute.append(attr)
                    for element in node.numeric:
                        child.numeric.append(element)
                    for element in node.categorical:
                        child.categorical.append(element)
                    node.children.append(child)
                    node.classIndex = None
                    node.probabilityIndex = None
                    node.examples = []

            if bestAttribute['type'] == 'categorical':
                ranges = Utils.retrieveSet(node.examples, bestAttribute['attribute'])
                for item in ranges:
                    child = Node('')
                    child.parent = node
                    child.split = {
                        'attribute': node.attribute['name'],
                        'type': 'categorical',
                        'value': item,
                    }
                    child.name = child.parent.name + ' .. ' + child.split['attribute'] + ' == ' + str(child.split['value'])
                    for attr in node.ignoredAttribute:
                        child.ignoredAttribute.append(attr)
                    for element in node.numeric:
                        child.numeric.append(element)
                    for element in node.categorical:
                        child.categorical.append(element)
                    node.children.append(child)
                    node.classIndex = None
                    node.probabilityIndex = None
                    node.examples = []

        return

    elif node.deadEnd: return

    else:

        numberOfDeadEnds = 0
        for child in node.children:
            if child.deadEnd: numberOfDeadEnds = numberOfDeadEnds + 1

        if numberOfDeadEnds == len(node.children):
            node.deadEnd = True

        if node.attribute['type'] == 'categorical':
            exampleAttributeValue = example[node.attribute['name']]
            for child in node.children:
                if child.split['value'] == exampleAttributeValue:
                    visitTree(child, example)
                    break
        if node.attribute['type'] == 'numeric':
            exampleAttributeValue = example[node.attribute['name']]
            for child in node.children:
                if child.split['min'] <= exampleAttributeValue <= child.split['max']:
                    visitTree(child, example)
                    break

    return


