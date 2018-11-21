import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix
import timeit, math, psutil, os
from sklearn.ensemble import RandomForestClassifier


def learn(trainFile, testFile, training_size):
    start = timeit.default_timer()
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

    # clf_entropy = DecisionTreeClassifier(criterion = "entropy",
    #                                  random_state = 100,
    #                                  max_depth=6,
    #                                  min_samples_leaf=.12,
    #                                  min_samples_split=.435)

    clf_entropy = RandomForestClassifier(n_estimators=10,
                                         random_state=100,
                                         criterion='entropy',
                                         max_depth=10,
                                         min_samples_leaf=.005,
                                         min_samples_split=.01)



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
    # list = [100]

    file = open(output, 'w')
    file.write(f'size, accuracy, precision, recall, fa, d2h, f1, time\n')

    for item in list:
        start = timeit.default_timer()
        result = learn(train, test, item)
        end = timeit.default_timer()
        file.write(f'{item}, {100*result[0]:.2f}, {100*result[1]:.2f}, {100*result[2]:.2f}, {100*result[3]:.2f}, {100*result[4]:.2f}, {100*result[5]:.2f}, {result[7]:.2f}\n')

    file.close()
    return


for x in range(1,11):
    datasets = ['abinit', 'lammps', 'libmesh', 'mda']
    datasets = ['abinit']
    path = '/home/rr/Workspace/NCSUFSS18/cp/datasets/'
    i = 0
    for set in datasets:
        dump(f'{path}{set}-train-{x}.csv', f'{path}{set}-test-{x}.csv', f'{set}-dump-rf-{x}.csv')
        i += 1

# dump('/home/rr/Workspace/NCSUFSS18/cp/datasets/abinit-train-1.csv', '/home/rr/Workspace/NCSUFSS18/cp/datasets/abinit-test-1.csv', 'abinit-dump-rf-exp.csv')
# dump('lammps-train.csv', 'lammps-test.csv', 'lammps-dump-rf.csv')
# dump('libmesh-train.csv', 'libmesh-test.csv','libmesh-dump-rf.csv')
# dump('mda-train.csv', 'mda-test.csv', 'mda-dump-rf.csv')



# i=0
# for x in range(1,101):
#     print(x)
#     datasets = ['abinit']
#     path = '/home/rr/Workspace/NCSUFSS18/cp/datasets/'
#     start = timeit.default_timer()
#     for set in datasets:
#         result = learn(f'{path}{set}-train-1.csv', f'{path}{set}-test-1.csv', x)
#     end = timeit.default_timer()
#     i = i + (end-start)
# print(i)

















# process = psutil.Process(os.getpid())
# memory = process.memory_info()[0] / float(2 ** 20)
# print(memory)
