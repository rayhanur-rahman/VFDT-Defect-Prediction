import sklearn.metrics as sk, math, sys, matplotlib.pyplot as plt, numpy as np, Utils

def example():
    x = [1, 2, 3, 10, 50, 100]
    y = [50, 90, 80, 10, 0, 50]

    print(sk.auc(x, y))

    year = [1960, 1970, 1980, 1990, 2000, 2010]
    pop_pakistan = [44.91, 58.09, 78.07, 107.7, 138.5, 170.6]
    pop_india = [449.48, 553.57, 696.783, 870.133, 1000.4, 1309.1]
    plt.plot(year, pop_pakistan, color='green', label='pak', marker='x')
    plt.plot(year, pop_india, color='orange', label='ind', marker='o')
    plt.xlabel('Countries')
    plt.ylabel('Population in million')
    plt.title('Pakistan India Population till 2010')
    plt.legend()
    # plt.show()
    plt.savefig('xx.png')
    return

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


def getAUCOfAll():
    dataset_list = ['abinit', 'lammps', 'libmesh', 'mda']
    learner_list = ['cart', 'fft', 'rf', 'vfdt']
    x_list = ['data-size', 'loc']
    y_list = ['accuracy', 'precision', 'recall', 'f1-score', 'd2h', 'training-time']

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

