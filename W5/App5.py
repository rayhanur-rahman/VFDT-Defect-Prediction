import math, random, Num, Sym, Rows, csv, Model, sys, Dicretizer, prettytable, Optimizer

print('unsupervised discretization on weatherLong.csv')
discretizer = Dicretizer.Unsupervised()
discretizer.discretize("weatherLong.csv", '$temp')
optimizer1 = Optimizer.Dom()
print("domination score of weatherLong.csv")
optimizer1.getScore("weatherLong.csv")
print("domination score of auto.csv")
optimizer1.getScore("auto.csv")
