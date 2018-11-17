import csv, re, Utils, math, sys, Node, timeit, random

# abinit: 6728971 19
# lammps: 15173205 19
# libmesh: 6565557 19
# mda: 1808907 14


def dump(csvFile):
    list = [.01, .02, .03, .04, .05, .06,
            .07, .08, .09, .1, .2, .3,
            .4, .5, .6, .7, .8, .9,
            1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
            80, 85, 90, 95, 100]
    file = open('temp.csv', 'w')
    file.write('loc\n')

    for item in list:
        streamIndex = 0
        loc = 0
        for row in Utils.csvRowsGenerator(csvFile):
            for index in range(0, len(row)):
                if index == 14:
                    loc = loc + float(row[index])
            streamIndex += 1
            if streamIndex >= item*10588*.01:
                file.write(f'{100*loc/1808907:.2f}\n')
                break
    file.close()
    return

dump('/home/rr/Workspace/NCSUFSS18/cp/mda-train.csv')

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

# trainTestSplit('/home/rr/Workspace/NCSUFSS18/cp/mda.csv', 'mda-train.csv', 'mda-test.csv')