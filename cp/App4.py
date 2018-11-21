import numpy as np, random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix
import timeit, math, psutil, os
from sklearn.ensemble import RandomForestClassifier


def learn(trainFile, testFile, training_size, depth, leaf, split, forest):
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
                                     max_depth=depth,
                                     min_samples_leaf=leaf,
                                     min_samples_split=split)

    # clf_entropy = RandomForestClassifier(n_estimators=forest,
    #                                      random_state=100,
    #                                      criterion='entropy',
    #                                      max_depth=depth,
    #                                      min_samples_leaf=leaf,
    #                                      min_samples_split=split)



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

def tune(data, size):
    print(f'{data} {size}')
    max = 0
    depth = 0
    leaf = 0
    split = 0
    forest = 0
    random.seed(0)
    for i in range(0, 100):
        x = random.randint(3,7)
        y = random.randint(1, 99)/200
        z = random.randint(1, 99)/100
        f = random.randint(1,10)*10
        # print(f'{i} {x} {y} {z}')
        out = learn(f'/home/rr/Workspace/NCSUFSS18/cp/datasets/{data}-train-1.csv', f'/home/rr/Workspace/NCSUFSS18/cp/datasets/{data}-test-1.csv', size, x, y, z, f)
        if out[2] > max:
            depth = x
            leaf = y
            split = z
            forest = f
            max = out[2]
            # print(max)

    print(f'{depth} {leaf} {split} {f} {max:.2f}')
    return

def de(fobj, bounds, mut=0.8, crossp=0.7, popsize=20, its=1000):
    dimensions = len(bounds)
    pop = np.random.rand(popsize, dimensions)
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]
    for i in range(its):
        # print(i)
        for j in range(popsize):
            idxs = [idx for idx in range(popsize) if idx != j]
            a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        yield best, fitness[best_idx]

def obj(args):
    out = learn(f'/home/rr/Workspace/NCSUFSS18/cp/datasets/abinit-train-1.csv',
                f'/home/rr/Workspace/NCSUFSS18/cp/datasets/abinit-test-1.csv', 10, math.floor(args[0]), args[1]/200, args[2]/100, math.floor(args[3]))
    return 100 - out[2]*100

print('abinit cart')
it = list(de(obj, bounds=[ (3,10), (1,49), (1,99), (10,100)  ], its=10))

for index in range(-1, -6, -1):
    depth = math.floor(it[index][0][0])
    leaf = it[index][0][1]/200
    split = it[index][0][2]/100
    forest = math.floor(it[index][0][3])
    recall = 100 - it[index][1]
    print(f'{depth}, {leaf:.2f}, {split:.2f}, {forest}, {recall:2f}')