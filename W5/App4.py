import math, random, Num, Sym, Rows, csv, Model, sys, Dicretizer

discretizer = Dicretizer.Unsupervised()
discretizer.discretize("weatherLong.csv", '$temp')