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
        self.exampleCount = 0
        self.deadEnd = False
        self.numeric = []
        self.categorical = []
        return

def preOrder(node):
    print(f'{node.exampleCount} # {node.classIndex} # {node.probabilityIndex} # {node.name}')
    if len(node.children) > 0:
        for child in node.children:
            preOrder(child)
    return

def computeStatistics(node):
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
    return

def recomputeStatistics(node, example):
    classNameOfTheExample = example['class']
    classIndex = node.classIndex
    probabilityIndex = node.probabilityIndex

    if classNameOfTheExample not in classIndex:
        classIndex.append(classNameOfTheExample)
        probabilityIndex.append(0)

    priorCountMatrix = [0] * len(classIndex)
    classMatrixIndex = 0
    for item in classIndex:
        priorCountMatrix[classMatrixIndex] = node.exampleCount * probabilityIndex[classMatrixIndex]
        if item == classNameOfTheExample:
            priorCountMatrix[classMatrixIndex] += 1
        probabilityIndex[classMatrixIndex] = (priorCountMatrix[classMatrixIndex] + .001) / (
                    node.exampleCount + 1 + .001)
        classMatrixIndex += 1
    return

def adaptForMissingSplits(node, example, minDepth, pushExamplesToLeaf, isAdaptive):
    if node.attribute['type'] == 'categorical':
        exampleAttributeValue = example[node.attribute['name']]
        child = Node('')
        child.parent = node
        child.split = {
            'attribute': node.attribute['name'],
            'type': 'categorical',
            'value': exampleAttributeValue,
        }
        child.name = child.parent.name + ' .. ' + child.split['attribute'] + ' == ' + str(child.split['value'])
        for attr in node.ignoredAttribute:
            child.ignoredAttribute.append(attr)
        for element in node.numeric:
            child.numeric.append(element)
        for element in node.categorical:
            child.categorical.append(element)
        node.children.append(child)
        node.examples = []
        visitTree(node, example, minDepth, pushExamplesToLeaf, isAdaptive)
        return

    if node.attribute['type'] == 'numeric':
        exampleAttributeValue = example[node.attribute['name']]
        minimumDistanceToSplit = sys.maxsize

        childToBeModified = None
        for child in node.children:
            if math.fabs(exampleAttributeValue - child.split['min']) < math.fabs(minimumDistanceToSplit):
                minimumDistanceToSplit = exampleAttributeValue - child.split['min']
                childToBeModified = child

        if minimumDistanceToSplit > 0:
            childToBeModified.split['max'] = minimumDistanceToSplit - childToBeModified.split['min']
        else:
            childToBeModified.split['min'] = childToBeModified.split['min'] + minimumDistanceToSplit

        visitTree(childToBeModified, example, minDepth, pushExamplesToLeaf, isAdaptive)
        return

    print('still I can not catch')
    return

def checkBound(node, minDepth):

    splits = []
    chunks = []

    for attr in node.ignoredAttribute:
        if attr['type'] == 'categorical':
            if attr['name'] in node.categorical: node.categorical.remove(attr['name'])
        if attr['type'] == 'numeric':
            if attr['name'] in node.numeric: node.numeric.remove(attr['name'])

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

    if len(node.ignoredAttribute) >= minDepth or len(splits) <= 1:
        if len(node.examples) > 49:
            node.deadEnd = True
        criticalPoint = 0

    elif len(splits) > 1:
        min = splits[0]['averageEntropy']
        max = splits[1]['averageEntropy']
        criticalPoint = (max - min)

    delta = .05
    unique = Utils.retrieveSet(node.examples, 'class')
    epsilon = math.log(len(unique), math.e) * math.sqrt((math.log(1 / delta, math.e)) / len(node.examples))
    return epsilon, criticalPoint, splits






def visitTree(node, example, minDepth, pushExamplesToLeaf, isAdaptive):

    if len(node.children) == 0:
        node.examples.append(example)
        node.exampleCount = node.exampleCount + 1

        # if len(node.examples) < 10: return

        # build statistics
        computeStatistics(node)

        # check for epsilon
        result = checkBound(node, minDepth)
        epsilon = result[0]
        criticalPoint = result[1]
        splits = result[2]
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
                    node.examples = []

        return

    elif node.deadEnd and not pushExamplesToLeaf:
        recomputeStatistics(node, example)
        node.exampleCount += 1
        return

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
                    visitTree(child, example, minDepth, pushExamplesToLeaf, isAdaptive)
                    return


        if node.attribute['type'] == 'numeric':
            exampleAttributeValue = example[node.attribute['name']]
            for child in node.children:
                if child.split['min'] <= exampleAttributeValue <= child.split['max']:
                    visitTree(child, example, minDepth, pushExamplesToLeaf, isAdaptive)
                    return

        if isAdaptive: adaptForMissingSplits(node, example, minDepth, pushExamplesToLeaf, isAdaptive)
        else:
            recomputeStatistics(node, example)
            node.exampleCount += 1

    return

def visiTreeForTest(node, example, hits, miss):
    if len(node.children) == 0:

        maxProbability = -sys.maxsize
        maxProbabilityIndex = None
        for pIndex in range(0, len(node.probabilityIndex)):
            if node.probabilityIndex[pIndex] > maxProbability:
                maxProbability = node.probabilityIndex[pIndex]
                maxProbabilityIndex = pIndex
        predictedClass = node.classIndex[maxProbabilityIndex]

        if predictedClass == example['class']:
            hits.append(1)
        else:
            miss.append(1)

        return

    else:
        if node.attribute['type'] == 'categorical':
            exampleAttributeValue = example[node.attribute['name']]
            for child in node.children:
                if child.split['value'] == exampleAttributeValue:
                    visiTreeForTest(child, example, hits, miss)
                    return


        if node.attribute['type'] == 'numeric':
            exampleAttributeValue = example[node.attribute['name']]
            for child in node.children:
                if child.split['min'] <= exampleAttributeValue <= child.split['max']:
                    visiTreeForTest(child, example, hits, miss)
                    return

        # calc
        # result = []
        maxProbability = -sys.maxsize
        maxProbabilityIndex = None
        for pIndex in range(0, len(node.probabilityIndex)):
            if node.probabilityIndex[pIndex] > maxProbability:
                maxProbability = node.probabilityIndex[pIndex]
                maxProbabilityIndex = pIndex
        predictedClass = node.classIndex[maxProbabilityIndex]

        if predictedClass == example['class']:
            hits.append(1)
        else:
            miss.append(1)

    return
