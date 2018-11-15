import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix

names = ['outlook', 'temp', 'humid', 'wind', 'play']
balance_data = pd.read_csv('weatherLong.csv',sep= ',\t', header=None, names=names)
balance_data = balance_data[['play', 'temp', 'humid', 'wind', 'outlook']]

print(balance_data.dtypes)
balance_data = pd.get_dummies(balance_data, columns=["outlook"])
print(balance_data)

print(balance_data.shape)


X = balance_data.values[:, 1:7]
Y = balance_data.values[:,0]

X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.15, random_state = 100)

clf_entropy = DecisionTreeClassifier(criterion = "entropy",
                                     random_state = 100,
                                     max_depth=3,
                                     min_samples_leaf=5)
clf_entropy.fit(X_train, y_train)

y_pred_en = clf_entropy.predict(X_test)

print(accuracy_score(y_test, y_pred_en))
print(confusion_matrix(y_test, y_pred_en))
print(classification_report(y_test, y_pred_en))


