import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix
import timeit, math, psutil, os

def learn(trainFile, testFile, training_size):
    balance_data = pd.read_csv(trainFile,sep= ',', header=None)
    balance_data_test = pd.read_csv(testFile,sep= ',', header=None)

    size = balance_data.shape[0]
    X = balance_data.values[0:math.ceil((training_size*size)/100), 1:]
    Y = balance_data.values[0:math.ceil((training_size*size)/100):,0]

    X2 = balance_data_test.values[:, 1:]
    Y2 = balance_data_test.values[:, 0]


    X_train = X
    X_test = X2
    y_train = Y
    y_test = Y2

    start = timeit.default_timer()
    clf_entropy = DecisionTreeClassifier(criterion = "entropy",
                                     random_state = 100,
                                     max_depth=3,
                                     max_leaf_nodes=20,
                                     min_samples_leaf=5,
                                     min_samples_split=10)

    clf_entropy.fit(X_train, y_train)
    end = timeit.default_timer()
    y_pred_en = clf_entropy.predict(X_test)

    ifa = 0
    tpFound = False
    for x in range(0, len(y_pred_en)):
        if y_pred_en[x] == 1.0 and y_test[x] == 0.0 and tpFound == False: ifa += 1
        if y_pred_en[x] == 1.0 and y_test[x] == 1.0: tpFound = True

    # print(f'accuracy: {accuracy_score(y_test, y_pred_en)}')
    cf = confusion_matrix(y_test, y_pred_en)
    # print(cf)
    # print(classification_report(y_test, y_pred_en))

    accuracy = (cf[1][1]+cf[0][0])/(cf[0][0]+cf[1][1]+cf[0][1]+cf[1][0])
    precision = cf[1][1]/(cf[1][1]+cf[0][1]+.001)
    recall = cf[1][1]/(cf[1][1]+cf[1][0])
    falseAlarm = cf[0][1]/(cf[0][1]+cf[0][0])
    d2h = math.sqrt((1-recall)*(1-recall) + falseAlarm*falseAlarm)
    f1score = (2*precision*recall)/(precision+recall+.001)

    return [accuracy, precision, recall, falseAlarm, d2h, f1score, ifa, (end-start)*1000]

def dump(train, test, output):
    print(train)

    list = [.01, .02, .03, .04, .05, .06,
            .07, .08, .09, .1, .2, .3,
            .4, .5, .6, .7, .8, .9,
            1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
            80, 85, 90, 95, 100]
    # list = [.01]

    file = open(output, 'w')
    file.write(f'data-size, accuracy, precision, recall, false-alarm, d2h, f1-score, ifa, training-time\n')

    for item in list:
        result = learn(train, test, item)
        file.write(f'{item}, {100*result[0]:.2f}, {100*result[1]:.2f}, {100*result[2]:.2f}, {100*result[3]:.2f}, {100*result[4]:.2f}, {100*result[5]:.2f}, {result[6]}, {100*result[7]:.2f}\n')

    file.close()
    return

dump('abinit-train.csv', 'abinit-test.csv', 'abinit-dump-cart.csv')
dump('lammps-train.csv', 'lammps-test.csv', 'lammps-dump-cart.csv')
dump('libmesh-train.csv', 'libmesh-test.csv','libmesh-dump-cart.csv')
dump('mda-train.csv', 'mda-test.csv', 'mda-dump-cart.csv')






















# process = psutil.Process(os.getpid())
# memory = process.memory_info()[0] / float(2 ** 20)
# print(memory)
