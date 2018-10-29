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
        return

def preOrder(node, list):
    # print(f'{node.name} {node.attribute} {node.split} {node.ignoredAttribute}')
    # print(f'{node.name} # {node.attribute} # {node.split} # {node.ignoredAttribute}')
    list.append(node)
    if len(node.children) > 0:
        for child in node.children:
            preOrder(child, list)
    return list

def visitTree(node, example, numeric, categorical):
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
        # print(f'2 {numeric}')
        # print(f'3 {categorical}')
        #
        for attr in node.ignoredAttribute:
            if attr['type'] == 'categorical':
                if attr['name'] in categorical: categorical.remove(attr['name'])
            if attr['type'] == 'numeric':
                if attr['name'] in numeric: numeric.remove(attr['name'])

        # print(f'4 {numeric}')
        # print(f'5 {categorical}')
        # print('###\n')

        for item in numeric:
            out = Utils.getBestSplitNumeric(node.examples, item)
            splits.append(out[0])
            for item in out[1]:
                chunks.append(item)

        for item in categorical:
            out = Utils.getBestSplitCategorical(node.examples, item)
            splits.append(out[0])
            for item in out[1]:
                chunks.append(item)

        splits.sort(key=lambda k: k['averageEntropy'])

        if len(splits) > 1:
            min = splits[0]['averageEntropy']
            max = splits[1]['averageEntropy']
            criticalPoint = (max - min)
        else:
            criticalPoint = 0
            print(f'all attribute processed')

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
                    node.children.append(child)
                    node.classIndex = None
                    node.probabilityIndex = None
                    node.examples = []

        return

    else:
        if node.attribute['type'] == 'categorical':
            exampleAttributeValue = example[node.attribute['name']]
            for child in node.children:
                if child.split['value'] == exampleAttributeValue:
                    visitTree(child, example, numeric, categorical)
                    break
        if node.attribute['type'] == 'numeric':
            exampleAttributeValue = example[node.attribute['name']]
            for child in node.children:
                if child.split['min'] <= exampleAttributeValue <= child.split['max']:
                    visitTree(child, example, numeric, categorical)
                    break


