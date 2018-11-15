import csv, re, Utils, math, sys, Node, timeit, random

# abinit: 7421221 19
# lammps: 16755210 19
# libmesh: 7301355 19
# mda: 2011819 14


def dump(csvFile):
    streamIndex = 0
    attributeIndex = 0
    loc = 0
    file = open('dump.csv', 'w')
    for row in Utils.csvRowsGenerator(csvFile):
        print(row)
    return

# dump('/home/rr/Workspace/NCSUFSS18/cp/mda.csv')

def trainTestSplit(csv, traindata, testdata):
    streamIndex = 0
    file = open(testdata, 'w')
    file2 = open(traindata, 'w')

    list = []
    for x in range(0, math.ceil(11705*.1), 1):
        list.append(random.randint(0, 11705))

    for row in Utils.csvRowsGenerator(csv):
        text = ''
        for item in row:
            if text != '': text = text + ', ' + str(item)
            else: text = str(item)
        if streamIndex in list: file.write(f'{text}\n')
        else: file2.write(f'{text}\n')

        streamIndex += 1
    file.close()
    file2.close()
    return

trainTestSplit('/home/rr/Workspace/NCSUFSS18/cp/mda.csv', 'mda-train.csv', 'mda-test.csv')