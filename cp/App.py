import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix
import timeit, math



# balance_data = pd.read_csv('/media/rr/8E30E13030E12047/bigdata/higgs.csv',sep= ',', header=None)


balance_data = pd.read_csv('bugs-test.csv',sep= ',', header=None)

# print(balance_data.dtypes)

print(balance_data.shape)


X = balance_data.values[:, 1:30]
Y = balance_data.values[:,0]



X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = .9999,
                                                     random_state = 100)

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

print(f'{accuracy:.2f} {precision:.2f} {recall:.2f} {falseAlarm:.2f} {d2h:.2f} {f1score:.2f}')
# print(f'{cf[1][1]} {cf[1][0]} {cf[0][1]} {cf[0][0]}')
# print(f'{end - start}')
