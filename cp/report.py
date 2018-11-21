import sklearn.metrics as sk, math, sys, matplotlib.pyplot as plot, numpy as np, Utils

def getAUC(csvFile, xName, yName):
    line = 0
    xIndex = 0
    yIndex = 0
    X = []
    Y = []
    for row in Utils.csvRowsGenerator(csvFile):
        for index in range(0, len(row), 1):
            if line == 0:
                if str(row[index]).strip() == xName:
                    xIndex = index
                if str(row[index]).strip() == yName:
                    yIndex = index
            else:
                if index == xIndex: X.append(float(str(row[index]).strip()))
                if index == yIndex: Y.append(float(str(row[index]).strip()))
        line += 1

    return sk.auc(X, Y)


def getAUCLoc(csvFile, xName, yName, percent):
    line = 0
    xIndex = 0
    yIndex = 0
    X = []
    Y = []
    for row in Utils.csvRowsGenerator(csvFile):
        for index in range(0, len(row), 1):
            if line == 0:
                if str(row[index]).strip() == xName:
                    xIndex = index
                if str(row[index]).strip() == yName:
                    yIndex = index
            else:
                if float(str(row[xIndex]).strip()) < percent:
                    if index == xIndex: X.append(float(str(row[index]).strip()))
                    if index == yIndex: Y.append(float(str(row[index]).strip()))
        line += 1
    # print(X)
    # print(Y)
    return sk.auc(X, Y)



def getAUCOfAll():
    dataset_list = ['abinit', 'lammps', 'libmesh', 'mda']
    learner_list = ['cart', 'fft', 'rf', 'vfdt']
    x_list = ['size', 'loc']
    y_list = ['precision', 'recall', 'time']

    file = open('auc-report.csv', 'w')
    file.write('dataset, learner, x-axis, y-axis, auc-score\n')
    for d in dataset_list:
        for x in x_list:
            for y in y_list:
                for l in learner_list:
                    path = f'/home/rr/Workspace/NCSUFSS18/cp/report/{d}-dump-{l}.csv'
                    auc = getAUC(path, x, y)
                    file.write(f'{d}, {l}, {x}, {y}, {auc:.2f}\n')

    file.close()
    return


def getPlot(learners, dataset, xName, yName):
    csvFiles = []

    for item in learners:
        csvFiles.append(f'/home/rr/Workspace/NCSUFSS18/cp/report/{dataset}-dump-{item}.csv')

    X = [None]*len(csvFiles)
    Y = [None]*len(csvFiles)

    for element in range(0, len(csvFiles), 1):
        line = 0
        xIndex = 0
        yIndex = 0
        X[element] = []
        Y[element] = []

        for row in Utils.csvRowsGenerator(csvFiles[element]):
            for index in range(0, len(row), 1):
                if line == 0:
                    if str(row[index]).strip() == xName:
                        xIndex = index
                    if str(row[index]).strip() == yName:
                        yIndex = index
                else:
                    if index == xIndex: X[element].append(float(str(row[index]).strip()))
                    if index == yIndex: Y[element].append(float(str(row[index]).strip()))
            line += 1

    plot.xlim(0, 100)
    plot.plot(X[0], Y[0], color='green', label='CART', marker='x')
    plot.plot(X[1], Y[1], color='red', label='FFT', marker='o')
    plot.plot(X[2], Y[2], color='blue', label='RF', marker='+')
    plot.plot(X[3], Y[3], color='black', label='VFDT', marker='s')
    plot.xlabel(f'{xName}')
    plot.ylabel(f'{yName}')
    plot.title(f'{dataset}: {xName} vs {yName}')
    plot.legend()
    # plot.show()
    plot.savefig(f'{dataset}-{xName}-{yName}.svg')
    plot.clf()
    return

# getPlot(['cart', 'fft', 'rf', 'vfdt'], 'libmesh', 'data-size', 'accuracy')

def getAllPlot():
    dataset_list = ['abinit', 'lammps', 'libmesh', 'mda']
    x_list = ['size']
    y_list = [ 'precision', 'recall', 'f1', 'time']

    for d in dataset_list:
        for x in x_list:
            for y in y_list:
                getPlot(['cart', 'fft', 'rf', 'vfdt'], d, x, y)

data = ['abinit', 'lammps', 'libmesh', 'mda']
learner = ['vfdt', 'cart', 'fft', 'rf']
for d in data:
    for l in learner:
        file = open(f'loc-auc-{d}-{l}.csv', 'w')
        file.write('loc, auc\n')
        for i in range(1, 11):
            x = getAUCLoc(f'/home/rr/Workspace/NCSUFSS18/cp/report/{d}-dump-{l}.csv', 'loc', 'recall', i*10)
            file.write(f'{i*10}, {x:.2f}\n')

        file.close()