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
    balance_data = pd.read_csv(trainFile,sep= ',', header=None)
    balance_data_test = pd.read_csv(testFile,sep= ',', header=None)

    size = balance_data.shape[0]
    X = balance_data.values[10001:, 1:]
    Y = balance_data.values[10001:, 0]

    X2 = balance_data_test.values[0:10000, 1:]
    Y2 = balance_data_test.values[0:10000, 0]


    X_train = X
    X_test = X2
    y_train = Y
    y_test = Y2

    start = timeit.default_timer()
    clf_entropy = DecisionTreeClassifier(criterion = "entropy",
                                     random_state = 100,
                                     max_depth=6,
                                     min_samples_leaf=50,
                                     min_samples_split=50)

    # clf_entropy = RandomForestClassifier(n_estimators=100,
    #                                      random_state=100,
    #                                      criterion='entropy',
    #                                      max_depth=6,
    #                                      min_samples_leaf=50,
    #                                      min_samples_split=50)



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



start = timeit.default_timer()

for x in range(0, 1):
    learn('/media/rr/8E30E13030E12047/bigdata/higgs.csv', '/media/rr/8E30E13030E12047/bigdata/higgs.csv', x+1)

end = timeit.default_timer()
print(f'{end-start}')



# process = psutil.Process(os.getpid())
# memory = process.memory_info()[0] / float(2 ** 20)
# print(memory)
