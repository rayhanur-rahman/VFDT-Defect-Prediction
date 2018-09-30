import Dicretizer
import Optimizer
import math, sys, Sym, Num, prettytable, Rows, Node, SupervisedDiscretizer

print(f'supervised discretization on weatherLong.csv')
disc = SupervisedDiscretizer.SupervisedDiscretizer("weatherLong.csv")
disc.discretizeAll()
print("\n\n")
print(f'supervised discretization on auto.csv')
disc = SupervisedDiscretizer.SupervisedDiscretizer("auto.csv")
disc.discretizeAll()