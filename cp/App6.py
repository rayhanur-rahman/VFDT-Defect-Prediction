import math, numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix

balance_data = pd.read_csv('bugs-test.csv',sep= ',', header=None)
# balance_data = pd.read_csv('/media/rr/8E30E13030E12047/bigdata/higgs.csv',sep= ',', header=None)


# print(balance_data.dtypes)

print(balance_data.shape)


X = balance_data.values[:, 1:30]
Y = balance_data.values[:,0]

X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.30, random_state = 100)

y_0 = (Y == 0)
y_train_0 = (y_train == 0)
y_test_0 = (y_test == 0)

y_1 = (Y == 1)
y_train_1 = (y_train == 1)
y_test_1 = (y_test == 1)


clf_entropy = DecisionTreeClassifier(criterion = "entropy",
                                     random_state = 100,
                                     max_depth=3,
                                     max_leaf_nodes=20,
                                     min_samples_leaf=5,
                                     min_samples_split=20)
clf_entropy.fit(X_train, y_train_1)

y_pred_en = clf_entropy.predict(X_test)

print(f'accuracy: {accuracy_score(y_test_1, y_pred_en)}')
cf = confusion_matrix(y_test_1, y_pred_en)
print(cf)
print(classification_report(y_test_1, y_pred_en))

# TN FP
# FN TP

accuracy = (cf[1][1]+cf[0][0])/(cf[0][0]+cf[1][1]+cf[0][1]+cf[1][0])
precision = cf[1][1]/(cf[1][1]+cf[0][1])
recall = cf[1][1]/(cf[1][1]+cf[1][0])
falseAlarm = cf[0][1]/(cf[0][1]+cf[0][0])
d2h = math.sqrt((1-recall)*(1-recall) + falseAlarm*falseAlarm)
f1score = (2*precision*recall)/(precision+recall)

print(f'{accuracy:.2f} {precision:.2f} {recall:.2f} {falseAlarm:.2f} {d2h:.2f} {f1score:.2f}')

