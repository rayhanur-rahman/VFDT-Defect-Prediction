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

# dump('/home/rr/Workspace/NCSUFSS18/cp/mda-train.csv')

def trainTestSplit(csv, traindata, testdata, seed):
    streamIndex = 0
    file = open(testdata, 'w')
    file2 = open(traindata, 'w')
    random.seed(seed)
    list = []
    for x in range(0, math.ceil(11705*.2), 1):
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

# for x in range(1, 11):
#     trainTestSplit('/home/rr/Workspace/NCSUFSS18/cp/mda.csv', f'mda-train-{x}.csv', f'mda-test-{x}.csv', x*100)


def average(dataset, learner):
    path = '/home/rr/Workspace/NCSUFSS18/cp/datasets/reports/'
    list = []
    for x in range(1,11):
        streamIndex = 0
        ls = []
        for row in Utils.csvRowsGenerator(f'{path}{dataset}-dump-{learner}-{x}.csv'):
            if streamIndex > 0:
                ls.append(row)
            streamIndex += 1
        list.append(ls)

    # list row col
    file = open(f'{dataset}-dump-{learner}.csv', 'w')
    file.write('size, accuracy, precision, recall, fa, d2h, f1, time\n')
    sum = 0
    string = ''
    for row in range(0, 39):
        for col in range(0,8):
            for x in range(0,10):
                value = float(str(list[x][row][col]).strip())
                sum = sum + value
            sum = sum/10
            if string != '': string = string + ', ' + f'{sum:.2f}'
            else: string = f'{sum:.2f}'
            sum=0
        file.write(f'{string}'+'\n')
        string=''
    file.close()
    return

average('abinit', 'rf')
average('lammps', 'rf')
average('libmesh', 'rf')
average('mda', 'rf')