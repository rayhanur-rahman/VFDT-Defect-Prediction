import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix

balance_data = pd.read_csv('d.csv',sep= ',', header=None)

# print(balance_data.dtypes)

print(balance_data.shape)


X = balance_data.values[:, 1:5]
Y = balance_data.values[:,0]

X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.3, random_state = 100)

clf_entropy = DecisionTreeClassifier(criterion = "entropy",
                                     random_state = 100,
                                     max_depth=3,
                                     min_samples_leaf=5)
clf_entropy.fit(X_train, y_train)

y_pred_en = clf_entropy.predict(X_test)

print(f'accuracy: {accuracy_score(y_test, y_pred_en)}')
print(confusion_matrix(y_test, y_pred_en))
print(classification_report(y_test, y_pred_en))


