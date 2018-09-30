import Dicretizer
import Optimizer

print('unsupervised discretization on weatherLong.csv')
discretizer = Dicretizer.Unsupervised()
result = discretizer.discretize("weatherLong.csv", '$temp')
print(result[1])

print('unsupervised discretization on auto.csv')
discretizer = Dicretizer.Unsupervised()
result = discretizer.discretize("auto.csv", '$horsepower')
print(result[1])

optimizer1 = Optimizer.Dom()

print("domination score of weatherLong.csv")
result = optimizer1.getScore("weatherLong.csv")
print(result[1])

print("domination score of auto.csv")
result = optimizer1.getScore("auto.csv")
print(result[1])
